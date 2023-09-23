from application import app, greet

def test_quick():
  a = "jeff"
  greeting = greet(a)
  assert greeting == "Hi jeff"
