Basic Recipe Server

1. Prepare a local virtual environment:
  make venv

2. Activate the environment:
  source venv/bin/activate

3. Run tests:
  make test

4. Run the server:
  make run


Future enhancements:
  - More tests covering edge cases, with as features or unit tests..
  - Add next/previous entries for the by-cruise endpoint.
  - Add create/delete endpoints.
  - Production server using uWSGI.
  - Enhance the swagger to allow 'start' parameter in Swagger UI.
