import sys
import os
from streamlit.web import cli as stcli

if __name__ == '__main__':
    # 1. Add the current directory to Python path so imports work
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    # 2. Tell Streamlit to run the dashboard file
    sys.argv = ["streamlit", "run", "ui/dashboard.py"]
    
    # 3. Launch
    sys.exit(stcli.main())