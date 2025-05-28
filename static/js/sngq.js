
document.addEventListener('DOMContentLoaded',
    () => {
//     document.getElementById('message-container').scrollTo({
//         top: document.body.scrollHeight,
//     });
    const centrifuge = new Centrifuge(`ws://${window.CENTRIFUGO_CONFIG.ws_url}/connection/websocket`, {
        token: window.CENTRIFUGO_CONFIG.token
    });

    const anscontainer = document.getElementById(`ans-container`);
    const anstemplate = document.querySelector(`[data-search="ans-template"]`);

    centrifuge.on('connecting', function (ctx) {
        console.log(`connecting: ${ctx.code}, ${ctx.reason}`);
    }).on('connected', function (ctx) {
        console.log(`connected over ${ctx.transport}`);
    }).on('disconnected', function (ctx) {
        console.log(`disconnected: ${ctx.code}, ${ctx.reason}`);
    }).connect();

    const sub = centrifuge.newSubscription(window.CENTRIFUGO_CONFIG.channel);

    sub.on('publication', function (ctx) {
        console.log(ctx);

        const newMessageElement = anstemplate.cloneNode(true)
        if (ctx.data.avatar_url && ctx.data.avatar_url.trim() !== "") {
            newMessageElement.querySelector('[data-search="ans-template-avatar"]').src = ctx.data.avatar_url;
        }
        newMessageElement.querySelector('[data-search="ans-template-rating"]').setAttribute('data-answer-id', ctx.data.id);
        newMessageElement.querySelector('[data-search="ans-template-upvote"]').setAttribute('data-answer-id', ctx.data.id);
        newMessageElement.querySelector('[data-search="ans-template-downvote"]').setAttribute('data-answer-id', ctx.data.id);
        newMessageElement.querySelector('[data-search="ans-template-content"]').textContent = ctx.data.content;
        newMessageElement.querySelector('[data-search="ans-template-flag"]').setAttribute("data-answer-id", ctx.data.id);
        console.log(ctx.data.disable)
        newMessageElement.querySelector(`[data-search="ans-template-flag"]`).disabled = !!ctx.data.disable;
        newMessageElement.classList.remove('d-none');
        anscontainer.appendChild(newMessageElement);
    }).on('subscribing', function (ctx) {
        console.log(`subscribing: ${ctx.code}, ${ctx.reason}`);
    }).on('subscribed', function (ctx) {
        console.log('subscribed', ctx);
    }).on('unsubscribed', function (ctx) {
        console.log(`unsubscribed: ${ctx.code}, ${ctx.reason}`);
    }).subscribe();
});