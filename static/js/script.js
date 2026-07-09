document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("chat-form");

    if (!form) return;

    const input = document.getElementById("message");
    const chatBox = document.getElementById("chat-box");

    form.addEventListener("submit", async function (e) {

        e.preventDefault();

        const message = input.value.trim();

        if (message === "") return;

        chatBox.innerHTML += `
            <div class="user">
                ${message}
            </div>
        `;

        input.value = "";

        chatBox.scrollTop = chatBox.scrollHeight;

        try {

            const response = await fetch("/send_message", {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    message: message
                })

            });

            const data = await response.json();

            chatBox.innerHTML += `
                <div class="bot">
                    ${data.reply}
                </div>
            `;

            chatBox.scrollTop = chatBox.scrollHeight;

        }

        catch (error) {

            chatBox.innerHTML += `
                <div class="bot">
                    Server Error!
                </div>
            `;

        }

    });

});


function clearChat() {

    const chatBox = document.getElementById("chat-box");

    chatBox.innerHTML = `
        <div class="bot">
            Chat cleared successfully.
        </div>
    `;
}