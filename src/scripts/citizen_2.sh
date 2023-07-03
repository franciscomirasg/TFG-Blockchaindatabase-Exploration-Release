docker run -d -e TAPLE_HTTPPORT=3002 \
	-e TAPLE_NETWORK_ADDR=/ip4/0.0.0.0/tcp \
	-e TAPLE_NETWORK_P2PPORT=40002 \
	-e TAPLE_NODE_SECRETKEY=0e61608e2a753e9bfb12eea4bbc110dc7fee22dcecb03eee0df6be8b2e66c113 \
	-e RUST_LOG=info \
	-e TAPLE_NETWORK_KNOWNNODES=/ip4/172.17.0.2/tcp/40000/p2p/12D3KooWKiBurMyAHiJ2UkBAy1ZoCwxXxpZHVjTA6D9YLT8cmdny \
	-p 3002:3002 \
	-p 40002:40002 \
	--name="citizen_2" \
	opencanarias/taple-client:0.1.4