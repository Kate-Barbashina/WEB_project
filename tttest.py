from flask import Flask, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def run():
    res = 0
    timer = 20
    if request.method == 'POST':
        res = int(request.form.get('result', 0))
        timer = int(request.form.get('timer_shadow', 0))
        if timer <= 0:
            return f'Final result {res}'
        res += 1

    return f"""
<html>
<head>
    <title>Test</title>
</head>
<body>
    <p id="timer">{timer}</p>
    <form action="/" id="vic" method="POST">
        <input type="number" readonly name="result" value="{res}">
        <input type="hidden" id="timer_shadow" name="timer_shadow" value="{timer}">
        <input type="submit"/>
    </form>
    <script>
        var x = setInterval(()=>{{
            var timer = parseInt(document.getElementById("timer").innerHTML);
            if (timer <= 0) {{
                clearInterval(x);
                document.getElementById("timer_shadow").value = "0";
                document.getElementById("vic").submit();
            }} else {{
                document.getElementById("timer_shadow").value = String(timer - 1);
                document.getElementById("timer").innerHTML = String(timer - 1);
            }}
        }}, 1000)
    </script>
</body>
</html>
"""


if __name__ == '__main__':
    app.run()