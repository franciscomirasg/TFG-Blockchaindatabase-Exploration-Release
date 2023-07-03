docker run -d -e TAPLE_HTTPPORT=3000 `
	-e TAPLE_NETWORK_ADDR=/ip4/0.0.0.0/tcp `
	-e TAPLE_NETWORK_P2PPORT=40000 `
	-e TAPLE_NODE_SECRETKEY=2daf002ddcf793fe73aa987fbf4aeddfca94bc89164d7a054c9bdb0b25407250 `
	-e RUST_LOG=info `
	-p 3000:3000 `
	-p 40000:40000 `
	--name="city_hall" `
	opencanarias/taple-client:0.1.4