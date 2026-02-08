<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Leonor Amor LLC Website</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            background-color: #f4f4f4;
            color: #333;
            margin: 20px;
        }

        h1, h2, h3 {
            color: #0044cc;
        }

        code {
            font-family: 'Courier New', monospace;
            background-color: #f9f9f9;
            padding: 5px;
            border-radius: 3px;
        }

        pre {
            background-color: #f9f9f9;
            padding: 20px;
            border-radius: 5px;
            white-space: pre-wrap;
            word-wrap: break-word;
            font-size: 1.1em;
        }

        pre code {
            display: block;
        }

        ul, ol {
            margin-left: 20px;
        }

        footer {
            margin-top: 30px;
            font-size: 0.9em;
            text-align: center;
            color: #777;
        }
    </style>
</head>
<body>
    <header>
        <h1>Leonor Amor LLC Website</h1>
        <p><strong>Created and maintained by Electric-i, LLC</strong></p>
    </header>

    <section>
        <h2>About the Project</h2>
        <p><strong>Leonor Amor LLC</strong> website built with <strong>Flask</strong>. View recent events, book consultations, and make an inquiry for <strong>Leonor Amor</strong></p>
    </section>

    <section>
        <h2>Requirements</h2>
        <h3>Prerequisites</h3>
        <ul>
            <li>Python 3.7+ (recommended: 3.8 or newer)</li>
            <li>pip (Python package installer)</li>
        </ul>

        <h3>Install Dependencies</h3>
        <ol>
            <li><strong>Clone the Repository:</strong>
                <pre><code>git clone https://gitlab.com/electric-i-llc/leonor-amor-llc.git
cd leonoramor.com</code></pre>
            </li>
            <li><strong>Create a Virtual Environment:</strong>
                <pre><code>python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`</code></pre>
            </li>
            <li><strong>Install the Required Dependencies:</strong>
                <pre><code>pip install -r requirements.txt</code></pre>
            </li>
        </ol>
    </section>

    <section>
        <h2>Setup Environment Variables</h2>
        <p>Some settings are stored in environment variables for security and configuration flexibility. Create a <code>.env</code> file in the project’s root directory and set the required environment variables as follows:</p>
        <pre><code>FLASK_APP=app.py          # Flask main application entry point
FLASK_ENV=development     # Can be "development", "production", or "testing"
SECRET_KEY=your-secret-key-here
DATABASE_URL=your-database-url-here
DEBUG=True                # Set to "False" in production
etc...
</code></pre>
        <p>Make sure to replace the values above with your actual values. For example, <code>SECRET_KEY</code> can be any random string, and <code>DATABASE_URL</code> is typically the URL of your database (e.g., PostgreSQL, SQLite).</p>
        <p>For extra security, ensure you <strong>never</strong> commit your <code>.env</code> file to version control. Add <code>.env</code> to your <code>.gitignore</code>:</p>
        <pre><code># .gitignore
.env</code></pre>
    </section>

    <section>
        <h2>Running the Application</h2>
        <p>To run the app in your local development environment:</p>
        <ol>
            <li><strong>Activate your virtual environment (if using):</strong>
                <pre><code>source venv/bin/activate  # On Windows: `venv\Scripts\activate`</code></pre>
            </li>
            <li><strong>Run Flask:</strong>
                <pre><code>flask run</code></pre>
                This will start the Flask development server, and you can visit the app at <code>http://localhost:5000</code>.
            </li>
        </ol>
    </section>

    <section>
        <h2>Creating <code>requirements.txt</code></h2>
        <p>If you want to regenerate the <code>requirements.txt</code> file with the current dependencies in your environment, run:</p>
        <pre><code>pip freeze > requirements.txt</code></pre>
    </section>

    <section>
        <h2>License</h2>
        <p>This project is licensed under the Apache License - see the <a href="LICENSE">LICENSE</a> file for details.</p>
    </section>

    <footer>
        <p>&copy; 2026 Leonor Amor LLC. Website and README created by Electric-i, LLC. All rights reserved.</p>
    </footer>
</body>
</html>
