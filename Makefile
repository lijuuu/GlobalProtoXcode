# Install necessary tools for protobuf compilation
GO_MODULE ?= $(shell go env GOPATH)
PROTO_DIRS := AuthUserAdminService ProblemsService

init:
	@echo "Initializing environment..."
	@export PATH=$PATH:$HOME/go/bin

install-tools:
	@echo "Installing necessary tools..."
	@go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
	@go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest
	@echo "Tools installed successfully."

generate-proto:
	@echo "Generating gRPC code from proto files..."
	@for dir in $(PROTO_DIRS); do \
		protoc -I=. \
			--go_out=. \
			--go_opt=paths=source_relative \
			--go-grpc_out=. \
			--go-grpc_opt=paths=source_relative \
			$$dir/*.proto; \
		mv *.pb.go $$dir/ 2>/dev/null || true; \
		mv *_grpc.pb.go $$dir/ 2>/dev/null || true; \
		echo "Generated proto for $$dir service"; \
	done

tidy:
	@go mod tidy

all: init install-tools generate-proto tidy

.PHONY: init install-tools generate-proto tidy all