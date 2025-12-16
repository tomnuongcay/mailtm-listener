# 📧 Mail.tm Listener Bot (VIP Edition)

This is a highly customized Python script designed to automate the process of creating temporary email addresses via the Mail.tm API and efficiently listening for incoming 6-digit verification codes. This tool features enhanced stability, random domain selection, and a user-friendly, color-coded command-line interface (CLI).

## ✨ Key Features

* **🎣 Dynamic Email Generation:** Automatically creates a temporary Mail.tm email address with a human-like, random username (e.g., `john.smith123@randomdomain.com`).
* **🔄 Random Domain Selector (Anti-Detection):** Dynamically fetches the list of active Mail.tm domains and selects a random one for each new email, preventing repeated usage of a single domain (e.g., `@comfythings.com`), which helps bypass simple anti-spam/anti-cheat filters.
* **🎨 Custom VIP Terminal UI:** Features a color-coded and aesthetically pleasing CLI using the `colorama` library for clear status updates (Success, Error, Waiting).
* **⏱️ Configurable Timeout:** Users can set a custom maximum waiting time (in seconds) for the verification code to arrive, defaulting to 5 minutes (300 seconds).
* **🔒 Optional Custom Password:** Users are prompted to set a custom password for the generated temporary email or use a secure default password.
* **🔁 Persistent Loop:** After each completed run (either success or timeout), the bot prompts the user to easily generate another temporary email without restarting the script.
* **🛡️ Robust Code Retrieval:** Efficiently searches the newest incoming email for the first 6-digit sequence (the verification code).

## 🚀 Getting Started

### Prerequisites

You need Python 3 installed on your system (tested on Ubuntu/WSL). The project requires the following Python libraries:
