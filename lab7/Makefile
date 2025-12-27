.PHONY: test test-race bench cover clean

test:
    go test ./internal/... -v

test-integration:
    go test ./tests/integration/... -v

test-race:
    go test ./... -race

bench:
    go test ./tests/benchmarks/... -bench=. -benchmem

cover:
    go test ./internal/... -coverprofile=coverage.out
    go tool cover -html=coverage.out -o coverage.html

clean:
    rm -f coverage.out coverage.html
    go clean -testcache

ci: test-race bench
