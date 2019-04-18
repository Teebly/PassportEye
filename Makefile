build-docker:
	docker build -t teebly/passport:`git rev-parse HEAD` .