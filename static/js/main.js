document.addEventListener('DOMContentLoaded', () => {
    // --- DOM Element References ---
    // Elements related to the URL shortening form (likely on index.html)
    const shortenForm = document.getElementById('shorten-form');
    const longUrlInput = document.getElementById('long-url');
    const customCodeInput = document.getElementById('custom-code');
    const messageArea = document.getElementById('message-area');
    const loadingSpinner = document.getElementById('loading-spinner');
    const shortenedUrlDisplay = document.getElementById('shortened-url-display');

    // Elements related to displaying a shortened URL and copy button (could be on shortened.html
    // or dynamically generated on index.html after shortening)
    const shortUrlTextElement = document.getElementById('short-url-text'); // For static display on shortened.html
    const copyButton = document.getElementById('copy-button'); // For static button on shortened.html

    // --- Helper Functions ---

    /**
     * Displays a temporary message to the user in the designated message area.
     * The message will automatically hide after a few seconds.
     * @param {string} type - The type of message ('success' or 'error'). Used for styling.
     * @param {string} message - The text content of the message.
     */
    function displayMessage(type, message) {
        if (!messageArea) {
            console.warn('Message area element not found.');
            return;
        }

        // Clear any existing messages
        messageArea.innerHTML = '';
        messageArea.style.display = 'block';

        // Create and append the new alert message
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type}`; // Assumes Bootstrap classes
        alertDiv.textContent = message;
        messageArea.appendChild(alertDiv);

        // Automatically hide the message after 5 seconds
        setTimeout(() => {
            messageArea.style.display = 'none';
            messageArea.innerHTML = ''; // Clear content
        }, 5000);
    }

    /**
     * Toggles the visibility of a loading spinner.
     * @param {boolean} isLoading - True to show the spinner, false to hide it.
     */
    function showLoading(isLoading) {
        if (loadingSpinner) {
            loadingSpinner.style.display = isLoading ? 'block' : 'none';
        }
    }

    /**
     * Validates a URL string using the native URL constructor.
     * @param {string} url - The URL string to validate.
     * @returns {boolean} - True if the URL is valid, false otherwise.
     */
    function isValidUrl(url) {
        try {
            new URL(url);
            return true;
        } catch (e) {
            return false;
        }
    }

    /**
     * Copies text to the clipboard and provides visual feedback on the button.
     * @param {string} text - The text content to copy to the clipboard.
     * @param {HTMLElement} buttonElement - The button element that triggered the copy action.
     */
    async function copyToClipboard(text, buttonElement) {
        if (!navigator.clipboard) {
            displayMessage('error', 'Clipboard API not supported by your browser. Please copy manually.');
            return;
        }

        try {
            await navigator.clipboard.writeText(text);
            const originalText = buttonElement.textContent;
            const originalClasses = buttonElement.className;

            // Provide visual feedback
            buttonElement.textContent = 'Copied!';
            buttonElement.classList.remove('btn-outline-secondary', 'btn-primary'); // Remove common button styles
            buttonElement.classList.add('btn-success');

            // Revert button text and style after a short delay
            setTimeout(() => {
                buttonElement.textContent = originalText;
                buttonElement.className = originalClasses; // Restore original classes
            }, 2000);
        } catch (err) {
            console.error('Failed to copy text: ', err);
            displayMessage('error', 'Failed to copy URL. Please copy manually.');
        }
    }

    // --- Event Listeners and Main Logic ---

    // 1. Handle URL Shortening Form Submission
    if (shortenForm) {
        shortenForm.addEventListener('submit', async (event) => {
            event.preventDefault(); // Prevent the browser's default form submission

            const longUrl = longUrlInput.value.trim();
            const customCode = customCodeInput.value.trim();

            // Client-side validation
            if (!longUrl) {
                displayMessage('error', 'Please enter a URL to shorten.');
                return;
            }
            if (!isValidUrl(longUrl)) {
                displayMessage('error', 'Please enter a valid URL (e.g., https://example.com).');
                return;
            }
            // Custom code validation: 3-20 alphanumeric characters, hyphens, or underscores
            if (customCode && !/^[a-zA-Z0-9_-]{3