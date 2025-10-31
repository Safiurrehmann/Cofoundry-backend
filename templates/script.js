// Particle System
class ParticleSystem {
    constructor(canvas) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.particles = [];
        this.resizeCanvas();
        window.addEventListener('resize', () => this.resizeCanvas());
        this.animate();
    }

    resizeCanvas() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }

    createParticle(x, y) {
        const particle = {
            x: x || Math.random() * this.canvas.width,
            y: y || Math.random() * this.canvas.height,
            vx: (Math.random() - 0.5) * 2,
            vy: (Math.random() - 0.5) * 2,
            radius: Math.random() * 2 + 1,
            opacity: Math.random() * 0.5 + 0.3,
            color: ['#6366f1', '#06b6d4', '#f97316'][Math.floor(Math.random() * 3)]
        };
        this.particles.push(particle);
    }

    update() {
        this.particles.forEach((particle, index) => {
            particle.x += particle.vx;
            particle.y += particle.vy;
            particle.opacity -= 0.01;

            if (particle.opacity <= 0) {
                this.particles.splice(index, 1);
            }

            if (particle.x < 0 || particle.x > this.canvas.width) {
                particle.vx *= -1;
            }
            if (particle.y < 0 || particle.y > this.canvas.height) {
                particle.vy *= -1;
            }
        });
    }

    draw() {
        this.particles.forEach(particle => {
            this.ctx.fillStyle = particle.color;
            this.ctx.globalAlpha = particle.opacity;
            this.ctx.beginPath();
            this.ctx.arc(particle.x, particle.y, particle.radius, 0, Math.PI * 2);
            this.ctx.fill();
        });
        this.ctx.globalAlpha = 1;
    }

    animate() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.update();
        this.draw();
        requestAnimationFrame(() => this.animate());
    }
}

// Initialize Particle System
const canvas = document.getElementById('particleCanvas');
const particleSystem = new ParticleSystem(canvas);

// Create particles on mouse move
document.addEventListener('mousemove', (e) => {
    if (Math.random() > 0.8) {
        particleSystem.createParticle(e.clientX, e.clientY);
    }
});

// Create particles on scroll
window.addEventListener('scroll', () => {
    if (Math.random() > 0.9) {
        particleSystem.createParticle(
            Math.random() * window.innerWidth,
            window.scrollY + Math.random() * window.innerHeight
        );
    }
});

// Anime.js Animations
anime.set('.title-word', {
    opacity: 0,
    translateY: 20
});

anime.stagger('.title-word', {
    targets: '.title-word',
    opacity: 1,
    translateY: 0,
    duration: 800,
    delay: anime.stagger(100),
    easing: 'easeOutExpo'
});

// Floating cards animation
anime({
    targets: '.card-1',
    translateY: [0, -30, 0],
    duration: 4000,
    loop: true,
    easing: 'easeInOutSine'
});

anime({
    targets: '.card-2',
    translateX: [0, 30, 0],
    duration: 5000,
    loop: true,
    easing: 'easeInOutSine'
});

anime({
    targets: '.card-3',
    rotate: [0, 360],
    duration: 6000,
    loop: true,
    easing: 'linear'
});

// Scroll animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            anime({
                targets: entry.target,
                opacity: [0, 1],
                translateY: [30, 0],
                duration: 800,
                easing: 'easeOutExpo'
            });
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

document.querySelectorAll('.about-card, .team-member, .faq-item').forEach(el => {
    observer.observe(el);
});

// FAQ Accordion
document.querySelectorAll('.faq-question').forEach(question => {
    question.addEventListener('click', () => {
        const faqItem = question.parentElement;
        const isActive = faqItem.classList.contains('active');

        document.querySelectorAll('.faq-item').forEach(item => {
            item.classList.remove('active');
        });

        if (!isActive) {
            faqItem.classList.add('active');
            anime({
                targets: faqItem,
                duration: 300,
                easing: 'easeOutExpo'
            });
        }
    });
});

// Contact Form
document.getElementById('contactForm').addEventListener('submit', (e) => {
    e.preventDefault();
    
    anime({
        targets: '.contact-form',
        scale: [1, 1.02, 1],
        duration: 600,
        easing: 'easeOutElastic(1, .6)'
    });

    setTimeout(() => {
        alert('Thank you for your message! We\'ll get back to you soon.');
        e.target.reset();
    }, 300);
});

// Smooth scroll for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth' });
        }
    });
});

// Hover glow effect on buttons
document.querySelectorAll('.cta-btn').forEach(btn => {
    btn.addEventListener('mouseenter', (e) => {
        anime({
            targets: btn,
            scale: 1.05,
            duration: 300,
            easing: 'easeOutQuad'
        });
    });

    btn.addEventListener('mouseleave', (e) => {
        anime({
            targets: btn,
            scale: 1,
            duration: 300,
            easing: 'easeOutQuad'
        });
    });
});

// Navbar scroll effect
let lastScrollTop = 0;
window.addEventListener('scroll', () => {
    const navbar = document.querySelector('.navbar');
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;

    if (scrollTop > 100) {
        navbar.style.background = 'rgba(15, 23, 42, 0.95)';
        navbar.style.boxShadow = '0 4px 20px rgba(99, 102, 241, 0.1)';
    } else {
        navbar.style.background = 'rgba(15, 23, 42, 0.8)';
        navbar.style.boxShadow = 'none';
    }

    lastScrollTop = scrollTop <= 0 ? 0 : scrollTop;
});

// Initialize animations on page load
window.addEventListener('load', () => {
    anime({
        targets: '.navbar',
        opacity: [0, 1],
        translateY: [-20, 0],
        duration: 800,
        easing: 'easeOutExpo'
    });
});