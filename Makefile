run:
	streamlit run research-buddy.py

install:
	pip3 install -r requirement.txt

docker-build:
	docker build . -t chatbot:${version}

docker-run:
	docker run chatbot:${version}