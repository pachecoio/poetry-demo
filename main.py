from poetry_demo import create_app

app = create_app()

if __name__ == "__main__":
    print("run app")
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000
    )