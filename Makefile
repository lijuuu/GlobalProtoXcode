# Install necessary tools for protobuf compilation
GO_MODULE ?= $(shell go env GOPATH)
PROTO_DIRS := AuthUserAdminService Compiler

# export GOENV_ROOT="$HOME/.goenv"
# export PATH="$GOENV_ROOT/bin:$PATH"
# eval "$(goenv init -)"

init:
	@echo "Initializing environment..."
	@if [ ! -d "$$HOME/go" ]; then \
		mkdir -p "$$HOME/go"; \
	fi
	@export GOPATH="$$HOME/go"
	@export PATH="$$PATH:$$GOPATH/bin"
	@if ! command -v go >/dev/null 2>&1; then \
		echo "Go is not installed. Please install Go first."; \
		exit 1; \
	fi

install-tools:
	@echo "Installing necessary tools..."
	@go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
	@go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest
	@echo "Tools installed successfully."

generate-proto:
	@echo "Generating gRPC code from proto files..."
	@for dir in $(PROTO_DIRS); do \
		protoc -I=. \
			--go_out=$$dir \
			--go-grpc_out=$$dir \
			$$dir/*.proto; \
		echo "Generated proto for $$dir service"; \
	done

tidy:
	@go mod tidy

all: init install-tools generate-proto tidy

.PHONY: init install-tools generate-proto tidy all