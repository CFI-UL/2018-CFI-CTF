from flask import Flask, render_template, request
from tempfile import NamedTemporaryFile, TemporaryDirectory
from subprocess import run
from json import dumps

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == "GET":
        return render_template("index.html")

    code = request.form['code']
    with TemporaryDirectory() as d:
        with NamedTemporaryFile(suffix=".hs", dir=d, delete=False) as f:
            f.write(code.encode())
            f.flush()
            out = run(["ghc", "-o", f"{d}/out", f.name], capture_output=True, cwd=d)
            if out.returncode != 0:
                ret = {"returncode": out.returncode, "stdout": out.stdout.decode(), "stderr": out.stderr.decode()}
                return dumps(ret, indent=4)
           
            for i in range(10):
                test = open(f"tests/input/{i}")
                out = run(f"{d}/out", capture_output=True, stdin=test, cwd=d)
                expected = "".join(open(f"tests/output/{i}").readlines())
                if out.stdout.decode().strip() != expected.strip():
                    test.seek(0)
                    ret = {
                            "returncode": out.returncode, 
                            "stdin": "".join(test.readlines()),
                            "stdout": out.stdout.decode(), 
                            "stderr": out.stderr.decode(), 
                            "expected": expected
                            }
                    return dumps(ret, indent=4)

            return dumps(open('flag').readline())


if __name__ == '__main__':
    app.run(host="0.0.0.0")
