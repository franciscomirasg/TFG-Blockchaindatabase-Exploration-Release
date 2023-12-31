docker run -d -e TAPLE_HTTPPORT=3003 `
	-e TAPLE_NETWORK_ADDR=/ip4/0.0.0.0/tcp `
	-e TAPLE_NETWORK_P2PPORT=40003 `
	-e TAPLE_NODE_SECRETKEY=4c8fabf15e73471629997057172e9a375d9073ae9129129128331536950bf58d `
	-e RUST_LOG=info `
	-e TAPLE_NETWORK_KNOWNNODES=/ip4/172.17.0.2/tcp/40000/p2p/12D3KooWKiBurMyAHiJ2UkBAy1ZoCwxXxpZHVjTA6D9YLT8cmdny `
	-p 3003:3003 `
	-p 40003:40003 `
	--name="recycle_company" `
	opencanarias/taple-client:0.1.4