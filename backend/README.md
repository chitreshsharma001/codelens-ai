# Backend README.md

# RepoInsight AI Backend

This is the backend component of the RepoInsight AI project, built using Flask. The backend serves as the API for the frontend application, providing endpoints to interact with repository data.

## Getting Started

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. Clone the repository:

   git clone https://github.com/yourusername/repoinsight-ai.git

2. Navigate to the backend directory:

   cd repoinsight-ai/backend

3. Install the required packages:

   pip install -r requirements.txt

### Running the Application

To run the Flask application, execute the following command:

```bash
python app/main.py
```

The application will start on `http://127.0.0.1:5000/` by default.

### Docker

To run the application using Docker, you can build and run the Docker container:

1. Build the Docker image:

   docker build -t repoinsight-ai-backend .

2. Run the Docker container:

   docker run -p 5000:5000 repoinsight-ai-backend

### API Endpoints

- `/api/repositories`: Get a list of repositories.
- `/api/repositories/<id>`: Get details of a specific repository.

### Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or features.

### License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.