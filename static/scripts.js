document.addEventListener('DOMContentLoaded', function() {
    const summaryContents = document.querySelectorAll('.summary-content');
    const maxLength = 300; // Define the maximum length for the summary

    summaryContents.forEach(content => {
        const summaryText = content.querySelector('.summary-text');
        const toggleBtn = content.querySelector('.toggle-btn');
        const paperBox = content.closest('.paper-box');

        if (summaryText.textContent.length > maxLength) {
            const originalText = summaryText.textContent;
            const truncatedText = originalText.substring(0, maxLength) + '...';

            summaryText.textContent = truncatedText;
            paperBox.style.height = 'auto'; // Reset height initially

            toggleBtn.addEventListener('click', function() {
                if (toggleBtn.textContent === 'Voir Plus') {
                    summaryText.textContent = originalText;
                    toggleBtn.textContent = 'Voir Moins';
                    toggleBtn.classList.add('expanded');
                    paperBox.style.height = 'auto'; // Expand height
                } else {
                    summaryText.textContent = truncatedText;
                    toggleBtn.textContent = 'Voir Plus';
                    toggleBtn.classList.remove('expanded');
                    paperBox.style.height = 'auto'; // Reset height
                }
            });
        } else {
            toggleBtn.style.display = 'none';
        }
    });
});
