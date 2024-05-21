# Video Generator App

The Video Generator App is a Streamlit-based application that allows users to generate story summaries and scripts based on provided topics using the OpenAI API, and then convert these scripts into videos using the NovitaAI API.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## Features

- Generate story summaries and scripts based on user-defined topics.
- Convert the generated scripts into videos using the NovitaAI API.
- Display and download the generated videos directly from the app.

## Requirements

- Python 3.8+
- Streamlit
- OpenAI
- Requests

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/yourusername/video-generator-app.git
   cd video-generator-app
   ```

2. Install the required Python packages:

  ```sh
  pip install -r requirements.txt
  ```

## Usage

1. Run the Streamlit application:

	```sh
	streamlit run app.py
	```
2. Open your web browser and go to http://localhost:8501.

3. Enter the story topic and click "Generate Story" to get the story summary and script.

4. Copy the generated Task ID and use it to download the video.

### Configuration
  In the sidebar, configure your API keys:

    - Enter your OpenAI API key.

    - Enter your NovitaAI API key.

### Contributing

  - Contributions are welcome! Please fork the repository and submit a pull request.


### License

  - This project is licensed under the MIT License.

