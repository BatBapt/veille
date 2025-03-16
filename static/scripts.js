document.addEventListener('DOMContentLoaded', function() {
    // Animation d'entrée pour les cartes
    const paperBoxes = document.querySelectorAll('.paper-box');
    paperBoxes.forEach((box, index) => {
        box.style.opacity = '0';
        box.style.transform = 'translateY(20px)';
        setTimeout(() => {
            box.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            box.style.opacity = '1';
            box.style.transform = 'translateY(0)';
        }, 100 * index);
    });

    // Fonctionnalité "Voir Plus/Moins" pour les résumés
    const toggleButtons = document.querySelectorAll('.toggle-btn');
    toggleButtons.forEach(button => {
        button.addEventListener('click', function() {
            const summaryText = this.previousElementSibling;
            summaryText.classList.toggle('expanded');

            if (summaryText.classList.contains('expanded')) {
                this.textContent = 'Voir Moins';
                // Animation de "typing" pour le texte qui apparaît
                const textToAnimate = summaryText.textContent;
                const visibleHeight = getComputedStyle(summaryText).maxHeight;
            } else {
                this.textContent = 'Voir Plus';
            }
        });
    });

    // Effet particules/connexions pour le fond (style IA/réseau)
    createNetworkBackground();

    // Animation pour les téléchargements
    const downloadButtons = document.querySelectorAll('.download-btn');
    downloadButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            // Animation de pulsation avant téléchargement
            this.classList.add('downloading');
            setTimeout(() => {
                this.classList.remove('downloading');
            }, 1000);
        });
    });
});

// Fonction pour créer le fond de type réseau/IA
function createNetworkBackground() {
    const container = document.querySelector('.container');
    const canvas = document.createElement('canvas');
    canvas.className = 'network-bg';
    canvas.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
        opacity: 0.15;
    `;
    document.body.appendChild(canvas);

    const ctx = canvas.getContext('2d');

    // Redimensionnement du canvas
    function resizeCanvas() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    // Création des nœuds
    const nodes = [];
    const nodeCount = Math.floor(window.innerWidth / 100); // Ajuste le nombre de nœuds selon la taille de l'écran

    class Node {
        constructor() {
            this.x = Math.random() * canvas.width;
            this.y = Math.random() * canvas.height;
            this.size = Math.random() * 2 + 1;
            this.speedX = (Math.random() - 0.5) * 0.5;
            this.speedY = (Math.random() - 0.5) * 0.5;
            this.connections = [];
        }

        update() {
            this.x += this.speedX;
            this.y += this.speedY;

            // Rebondir sur les bords
            if (this.x < 0 || this.x > canvas.width) this.speedX *= -1;
            if (this.y < 0 || this.y > canvas.height) this.speedY *= -1;
        }

        draw() {
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
            ctx.fillStyle = '#64ffda';
            ctx.fill();
        }
    }

    // Initialiser les nœuds
    for (let i = 0; i < nodeCount; i++) {
        nodes.push(new Node());
    }

    // Animation
    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Mettre à jour et dessiner les nœuds
        nodes.forEach(node => {
            node.update();
            node.draw();
        });

        // Dessiner les connexions
        ctx.strokeStyle = 'rgba(65, 105, 225, 0.3)';
        ctx.lineWidth = 0.5;

        for (let i = 0; i < nodes.length; i++) {
            for (let j = i + 1; j < nodes.length; j++) {
                const dx = nodes[i].x - nodes[j].x;
                const dy = nodes[i].y - nodes[j].y;
                const distance = Math.sqrt(dx * dx + dy * dy);

                if (distance < 150) { // Distance maximale pour une connexion
                    ctx.beginPath();
                    ctx.moveTo(nodes[i].x, nodes[i].y);
                    ctx.lineTo(nodes[j].x, nodes[j].y);

                    // Opacité basée sur la distance
                    const opacity = 1 - (distance / 150);
                    ctx.strokeStyle = `rgba(65, 105, 225, ${opacity * 0.5})`;

                    ctx.stroke();
                }
            }
        }

        requestAnimationFrame(animate);
    }

    animate();
}

// Ajout d'un effet de "typing" aux boutons
const buttons = document.querySelectorAll('button, .download-btn');
buttons.forEach(button => {
    button.addEventListener('mouseover', function() {
        this.style.transition = 'all 0.3s ease';
        this.style.letterSpacing = '1px';
    });

    button.addEventListener('mouseout', function() {
        this.style.letterSpacing = 'normal';
    });
});

// Détection de scroll pour effets parallaxe
window.addEventListener('scroll', function() {
    const scrollPosition = window.scrollY;
    const paperBoxes = document.querySelectorAll('.paper-box');

    paperBoxes.forEach((box, index) => {
        const boxPosition = box.getBoundingClientRect().top;
        const windowHeight = window.innerHeight;

        // Effet parallaxe subtil pour les boîtes
        if (boxPosition < windowHeight * 0.9) {
            const intensity = (windowHeight - boxPosition) / windowHeight * 0.05;
            box.style.transform = `translateY(${-intensity * 10}px)`;
        }
    });
});