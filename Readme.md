Devot challenge

Hello! If you are reading this then you are looking for information about this project and how to successfully start it. This is my Devot challenge solution as an entry coding challenge for Devot company. Before you start, there will be 2 different ways on how to start and test the project, depending on your OS. But before both, you should open the project in your editor of choice and start a new terminal.

WINDOWS

If you see 'PS' at the beginning of your terminal prompt, you first need to run the following command which allows you to create a virtual environment:

    Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass


If there is no 'PS' at the beginning of your terminal prompt, you can proceed with the following steps.


After running the command above, you can create your own virtual environment with the following command:

    venv\Scripts\activate

After which you should install the required pip packages located in requirements.txt with the following command:

    pip install -r requirements.txt

Great! Now that you have successfully completed the steps above you can start the program with this command:

    python -m uvicorn main:app --reload


Linux/macOS

If you are using Linux or macOS, create your own virtual environment with the following command:

    python3 -m venv venv

Then, you can start that virtual environment with:

    source venv/bin/activate

After which you should install the required pip packages located in requirements.txt with the following command:

    pip install -r requirements.txt

Great! Now that you have successfully completed the steps above you can start the program with this command:

    python -m uvicorn main:app --reload
