class TableNotFoundException(RuntimeError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



if __name__ == "__main__":
    print("\n"*3+ "Please launch the file labeled main_script.py" +"\n"*3)
