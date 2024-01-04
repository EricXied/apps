function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function dragwindow(title, window) {
    const titleBar = document.getElementById(title);
    const myWindow = document.getElementById(window);

    let isDragging = false;
    let dragOffsetX, dragOffsetY;

    titleBar.addEventListener('mousedown', function (e) {
        isDragging = true;
        dragOffsetX = e.clientX - myWindow.offsetLeft;
        dragOffsetY = e.clientY - myWindow.offsetTop;
    });

    document.addEventListener('mousemove', function (e) {
        if (isDragging) {
            myWindow.style.left = e.clientX - dragOffsetX + 'px';
            myWindow.style.top = e.clientY - dragOffsetY + 'px';
        }
    });

    document.addEventListener('mouseup', function () {
        isDragging = false;
    });
}

document.addEventListener('DOMContentLoaded', function () {
    const options = document.querySelector('.options');
    const openButton = document.querySelectorAll('.dot-icon');
    const newpost = document.querySelector('.write-post')
    const newform = document.querySelector('.new-form')
    const upload_buttom = document.querySelector('#upload')
    const file = document.querySelector('#upfile')

    dragwindow("window-title", "new-window")

    upload_buttom.addEventListener('click', () => {
        file.click()
    })

    file.addEventListener('change', () => {
        upload_buttom.innerText = `Selected File: ${file.files[0].name}`
    })

    newpost.addEventListener('click', () => {

        newform.style.visibility = "inherit";
        event.stopPropagation()
    })

    document.addEventListener('click', function (event) {
        if (!newform.contains(event.target)) {
            newform.style.visibility = "hidden";
        };

        if (options.classList.contains('options--active')) {

            if (!options.contains(event.target)) {
                options.classList.remove('options--active');
            }
        }
    });



    openButton.forEach(dotIcon => {
        dotIcon.addEventListener('click', (event) => {
            const clickedElement = event.target;
            let topmostElementWithName = null;
            let currentElement = clickedElement;

            while (currentElement !== null) {
                if (currentElement.getAttribute('name')) {
                    topmostElementWithName = currentElement;
                }
                currentElement = currentElement.parentElement;
            }

            const op1 = options.querySelector('#op1');
            const op2 = options.querySelector('#op2');
            op1['href'] = `/article/${topmostElementWithName.getAttribute('name')}`;
            op2['href'] = `/delete/${topmostElementWithName.getAttribute('name')}`;
            const x = dotIcon.offsetLeft;
            const y = dotIcon.offsetTop;

            options.classList.add('options--active');
            options.style.top = `${y}px`;
            options.style.left = `${x}px`;
            event.stopPropagation()
        });

    });
});

class Chatbox {
    constructor() {
        this.args = {
            openButton: document.querySelector('.chatbox__button'),
            chatBox: document.querySelector('.chatbox__support'),
            sendButton: document.querySelector('.send__button')
        };
        this.state = false;
        this.messages = [];


    }

    display() {
        const { openButton, chatBox, sendButton } = this.args;

        openButton.addEventListener('click', () => {
            this.toggleState(chatBox);
        });
        sendButton.addEventListener('click', () => {
            this.onSendButton(chatBox);
        });

        const node = chatBox.querySelector('input');
        node.addEventListener('keyup', ({ key }) => {
            if (key === 'Enter') {
                this.onSendButton(chatBox)
            }
        })
    }

    toggleState(chatbox) {
        this.state = !this.state;
        if (this.state) {
            chatbox.classList.add('chatbox--active')
            // chatbox.parentElement.style.visibility = "inherit"
        } else {
            chatbox.classList.remove('chatbox--active')
            // chatbox.parentElement.style.visibility = "hidden"
        }
    }

    onSendButton(chatbox) {
        var textField = chatbox.querySelector('input');
        let text1 = textField.value;
        if (text1 === "") {
            return;
        }
        const csrftoken = getCookie('csrftoken');
        let msg1 = { name: "User", message: text1 }
        this.messages.push(msg1);
        console.log(JSON.stringify({ message: text1 }))
        fetch('/predict', {
            method: 'POST',
            body: JSON.stringify({ message: text1 }),
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
        })
            .then(r => r.json())
            .then(r => {
                let msg2 = { name: "Sam", message: r.answer };
                this.messages.push(msg2);
                this.updateChatText(chatbox);
                textField.value = ''
            }).catch((error) => {
                console.error('Error:', error);
                this.updateChatText(chatbox);
                textField.value = ''

            });
    }

    updateChatText(chatbox) {
        var html = '';
        this.messages.slice().reverse().forEach(function (item, index) {
            if (item.name === "Sam") {
                html += '<div class="messages__item messages__item--visitor">' + item.message + '</div>'
            }
            else {
                html += '<div class="messages__item messages__item--operator">' + item.message + '</div>'
            }
        });
        const chatmessage = chatbox.querySelector('.chatbox__messages');
        chatmessage.innerHTML = html;

    }
}

const chatbox = new Chatbox();
chatbox.display();

