window.onload = function() {
    config = {{ particles_config }}
    config['selector'] = '.background';
    Particles.init(config);
};