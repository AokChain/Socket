# AOK Socket

Simple socket.io backend for receiving updateds about AOK blockchain.

`gunicorn app:app -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 1 --bind 0.0.0.0:6600`
