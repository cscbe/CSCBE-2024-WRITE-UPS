FROM lukemathwalker/cargo-chef:latest as chef
WORKDIR /app

FROM chef AS planner
COPY ./server/Cargo.toml ./server/Cargo.lock ./
COPY ./server/src ./src
RUN cargo chef prepare

FROM chef AS builder
COPY --from=planner /app/recipe.json .
RUN cargo chef cook --release
COPY ./server .
RUN cargo build --release
RUN mv ./target/release/server ./app

FROM debian:stable-slim AS runtime
WORKDIR /app
COPY --from=builder /app/app /usr/local/bin/
COPY ./server/certs /app/certs
EXPOSE 443
ENTRYPOINT ["/usr/local/bin/app"]
