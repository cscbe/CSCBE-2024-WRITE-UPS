use serde::{Deserialize, Serialize};
// use uuid::Uuid;

// use async_throttle::MultiRateLimiter;
// use std::sync::Arc;

use async_trait::async_trait;
// use std::time::Duration;
use time::Duration;
use time::OffsetDateTime;

// use tower::ServiceBuilder;

use tower_http::trace::TraceLayer;
use tower_sessions::{Expiry, MemoryStore, Session, SessionManagerLayer};

use http::request::Parts;

use axum::{
    extract::{FromRequestParts, Host},
    handler::HandlerWithoutStateExt,
    http::{StatusCode, Uri},
    response::{IntoResponse, Redirect},
    routing::{get, post},
    BoxError, Json, Router,
};
use axum_server::tls_rustls::RustlsConfig;
use std::{fmt, net::SocketAddr, path::PathBuf};
use tracing_subscriber::util::SubscriberInitExt;

#[allow(dead_code)]
#[derive(Clone, Copy)]
struct Ports {
    http: u16,
    https: u16,
}

#[tokio::main]
async fn main() {
    // initialize tracing
    tracing_subscriber::fmt()
        // .with_max_level(tracing::Level::DEBUG)
        .init();

    // Allow bursts with up to five requests per IP address
    // and replenishes one element every two seconds
    // We Box it because Axum 0.6 requires all Layers to be Clone
    // and thus we need a static reference to it
    // https://docs.rs/tower_governor/latest/tower_governor/#modules
    // let governor_conf = Box::new(
    //     GovernorConfigBuilder::default()
    //         .per_second(1)
    //         .burst_size(5)
    //         .key_extractor(SmartIpKeyExtractor)
    //         .finish()
    //         .unwrap(),
    // );
    // let governor_limiter = governor_conf.limiter().clone();
    // let interval = std::time::Duration::from_secs(60);
    // // a separate background task to clean up
    // std::thread::spawn(move || loop {
    //     std::thread::sleep(interval);
    //     tracing::info!("rate limiting storage size: {}", governor_limiter.len());
    //     governor_limiter.retain_recent();
    // });

    let ports = Ports {
        http: 80,
        https: 443,
    };
    // optional: spawn a second server to redirect http requests to this server
    tokio::spawn(redirect_http_to_https(ports));

    // configure certificate and private key used by https
    let certpath = PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .join("certs")
        .join("cert.pem");
    let keypath = PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .join("certs")
        .join("key.pem");
    let config = RustlsConfig::from_pem_file(certpath, keypath)
        .await
        .unwrap();

    let session_store = MemoryStore::default();
    let session_layer = SessionManagerLayer::new(session_store)
        .with_secure(false)
        .with_expiry(Expiry::OnInactivity(Duration::hours(10)));

    // build our application with a route
    let app = Router::new()
        // `GET /` goes to `root`
        .route("/", get(root))
        .route("/create_session", post(create_game_session))
        .route("/register_blob_capture", post(register_blob_capture))
        .layer(session_layer)
        // .layer(GovernorLayer {
        //     // We can leak this because it is created once and then
        //     config: Box::leak(governor_conf),
        // })
        .layer(TraceLayer::new_for_http());

    // run our app with hyper
    // `axum::Server` is a re-export of `hyper::Server`
    let addr = SocketAddr::from(([0, 0, 0, 0], ports.https));
    tracing::debug!("listening on {}", addr);

    axum_server::bind_rustls(addr, config)
        .serve(app.into_make_service())
        .await
        .unwrap();

    // let listener = TcpListener::bind(addr).await.unwrap();
    // axum::serve(
    //     listener,
    //     app.into_make_service_with_connect_info::<SocketAddr>(),
    // )
    // .await
    // .unwrap();

    // run our app with hyper
    // let listener = tokio::net::TcpListener::bind("127.0.0.1:3000")
    //     .await
    //     .unwrap();
    // tracing::debug!("listening on {}", listener.local_addr().unwrap());
    // axum::serve(listener, app).await.unwrap();
}

#[allow(dead_code)]
async fn redirect_http_to_https(ports: Ports) {
    fn make_https(host: String, uri: Uri, ports: Ports) -> Result<Uri, BoxError> {
        let mut parts = uri.into_parts();

        parts.scheme = Some(axum::http::uri::Scheme::HTTPS);

        if parts.path_and_query.is_none() {
            parts.path_and_query = Some("/".parse().unwrap());
        }

        let https_host = host.replace(&ports.http.to_string(), &ports.https.to_string());
        parts.authority = Some(https_host.parse()?);

        Ok(Uri::from_parts(parts)?)
    }

    let redirect = move |Host(host): Host, uri: Uri| async move {
        match make_https(host, uri, ports) {
            Ok(uri) => Ok(Redirect::permanent(&uri.to_string())),
            Err(error) => {
                tracing::warn!(%error, "failed to convert URI to HTTPS");
                Err(StatusCode::BAD_REQUEST)
            }
        }
    };

    let addr = SocketAddr::from(([127, 0, 0, 1], ports.http));
    let listener = tokio::net::TcpListener::bind(addr).await.unwrap();
    tracing::debug!("listening on {}", listener.local_addr().unwrap());
    axum::serve(listener, redirect.into_make_service())
        .await
        .unwrap();
}

// basic handler that responds with a static string
// async fn root() -> &'static str {
async fn root() -> impl IntoResponse {
    (StatusCode::OK, "Hello, World!")
}

const COUNTER_KEY: &str = "counter";

#[derive(Default, Deserialize, Serialize)]
struct Counter(usize);

#[derive(Clone, Deserialize, Serialize)]
struct GuestData {
    valid_session: bool,
    pageviews: usize,
    first_seen: OffsetDateTime,
    last_seen: OffsetDateTime,
}

impl Default for GuestData {
    fn default() -> Self {
        Self {
            valid_session: false,
            pageviews: 0,
            first_seen: OffsetDateTime::now_utc(),
            last_seen: OffsetDateTime::now_utc(),
        }
    }
}

struct Guest {
    session: Session,
    guest_data: GuestData,
}

impl Guest {
    const GUEST_DATA_KEY: &'static str = "guest.data";

    fn valid_session(&self) -> bool {
        self.guest_data.valid_session
    }

    async fn validate_session(&mut self) {
        self.guest_data.valid_session = true;
        Self::update_session(&self.session, &self.guest_data).await
    }
    async fn invalidate_session(&mut self) {
        self.guest_data.valid_session = false;
        Self::update_session(&self.session, &self.guest_data).await
    }

    fn first_seen(&self) -> OffsetDateTime {
        self.guest_data.first_seen
    }

    fn last_seen(&self) -> OffsetDateTime {
        self.guest_data.last_seen
    }

    fn pageviews(&self) -> usize {
        self.guest_data.pageviews
    }

    async fn mark_pageview(&mut self) {
        self.guest_data.pageviews += 1;
        Self::update_session(&self.session, &self.guest_data).await
    }

    async fn update_session(session: &Session, guest_data: &GuestData) {
        session
            .insert(Self::GUEST_DATA_KEY, guest_data.clone())
            .await
            .unwrap()
    }
}

impl fmt::Display for Guest {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.debug_struct("Guest")
            .field("valid_session", &self.valid_session())
            .field("pageviews", &self.pageviews())
            .field("first_seen", &self.first_seen())
            .field("last_seen", &self.last_seen())
            .finish()
    }
}

#[async_trait]
impl<S> FromRequestParts<S> for Guest
where
    S: Send + Sync,
{
    type Rejection = (StatusCode, &'static str);

    async fn from_request_parts(req: &mut Parts, state: &S) -> Result<Self, Self::Rejection> {
        let session = Session::from_request_parts(req, state).await?;

        let mut guest_data: GuestData = session
            .get(Self::GUEST_DATA_KEY)
            .await
            .unwrap()
            .unwrap_or_default();

        guest_data.last_seen = OffsetDateTime::now_utc();

        Self::update_session(&session, &guest_data).await;

        Ok(Self {
            session,
            guest_data,
        })
    }
}

const ALLOWED_HASH: &str = "7d11ae645deb20db7d5a155c45869e0b517e5d675eee3c512e65f7aa818097c5";

async fn create_game_session(
    // this argument tells axum to parse the request body
    // as JSON into a `CreateUser` type
    mut guest: Guest,
    Json(payload): Json<CreateSession>,
) -> (StatusCode, Json<GameSession>) {
    println!("Game start attempt: {}", payload.integrity_hash);

    if payload.integrity_hash != ALLOWED_HASH {
        guest.invalidate_session().await;
        println!("  ! Invalid hash");
        return (
            StatusCode::SERVICE_UNAVAILABLE,
            Json(GameSession {
                status: "game has been modified!".to_string(),
            }),
        );
    }

    // insert your application logic here
    //let user = User {
    //    id: 1337,
    //    username: payload.username,
    //};
    guest.validate_session().await;
    println!("  Start validated");

    let game_session = GameSession {
        status: "success".to_string(),
    };

    // this will be converted into a JSON response
    // with a status code of `201 Created`
    (StatusCode::CREATED, Json(game_session))
}

#[derive(Deserialize)]
struct BlobInfo {
    idx: usize,
    hash: String,
}
#[derive(Serialize)]
struct BlobResult {
    idx: usize,
    confirm_hash: String,
    message: String,
}
async fn register_blob_capture(
    _session: Session,
    mut guest: Guest,
    Json(payload): Json<BlobInfo>,
) -> (StatusCode, Json<BlobResult>) {
    println!(
        "Monster validation attempt: {} - {}",
        payload.idx, payload.hash
    );

    if !guest.valid_session() {
        println!("  ! Invalid sesion");
        return (
            StatusCode::FORBIDDEN,
            Json(BlobResult {
                idx: payload.idx,
                confirm_hash: "Not a valid session".to_string(),
                message: "".to_string(),
            }),
        );
    }

    // TODO, replace these with the actual ones
    let monster_hashes = vec![
        "57a90933caffa08d971dba2932c540b0424d2ff393a27b1a7a8b7cff4b9791f0",
        "ce2474c1c959a3bbea51b92137ece112a3579556e51a1f02e25a6bcf3277f9b8",
        "055e52f1fece50e5463ec388fad589a95bd59b0a06c4edd7fe847fbb49d6cb3f",
    ];
    // Used to verify the new hashes
    let confirm_hash = vec![
        "mqXKp7pPiUnbiNSU4FdEAR5DqHbQtVm7",
        "YyueVEmEEDrzooRLryS5PyyQqjLj2w5q",
        "qzaV4EYukjDJma39UocdutSm7dLysze7",
    ];
    let message = vec![
        "Beneath the digital moonlight, the code whispers secrets unheard by the many.",
        "Only those who dare to listen, weaving through the shadows, will unveil the path.",
        "Hidden and secret, the flag awaits: CSC{M00NLIgHT_MYs7erY_ESc@Pe}.",
    ];

    if monster_hashes[payload.idx] == payload.hash {
        println!("  Valid blob hash");

        let res = BlobResult {
            idx: payload.idx,
            confirm_hash: confirm_hash[payload.idx].to_string(),
            message: message[payload.idx].to_string(),
        };
        return (StatusCode::OK, Json(res));
    } else {
        guest.invalidate_session().await;
        println!("  Invalid blob hash");

        return (
            StatusCode::FORBIDDEN,
            Json(BlobResult {
                idx: payload.idx,
                confirm_hash: "Game modified or bypassed".to_string(),
                message: "".to_string(),
            }),
        );
    }
}

// the input to our `create_user` handler
#[derive(Deserialize)]
struct CreateSession {
    integrity_hash: String,
}

// // the output to our `create_user` handler
#[derive(Serialize)]
struct GameSession {
    status: String, // id: u64,
                    // username: String,
}
