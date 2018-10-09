all: bin/solution

bin/solution: src/solution.hs
	[ -d bin ] || mkdir bin
	ghc -o ./bin/solution -outputdir ./bin ./src/solution.hs

clean:
	rm -rf ./bin
