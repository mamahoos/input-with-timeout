from .console_output import cout, endl
import builtins, types, typing


def windows_input_with_timeout(prompt, timeout):
    cout << prompt              # Print the prompt to the console

    CR = chr(0x0D)              # Carriage return character
    LF = chr(0x0A)              # Line feed character 
    BS = chr(0x08)              # Backspace character
    SP = chr(0x20)              # Space character 
    ET = chr(0x03)              # End of text character
    HT = chr(0x09)              # Horizontal Tab character
    
    TAB_SIZE = 4                
    DELAY = 5e-2                # 50 ms
    line  = ''                  # Initialize an empty line buffer
    start = time.monotonic()
    end   = start + timeout     # Calculate the end time for the timeout

    while (time.monotonic() < end):
        if msvcrt.kbhit():              # If a key has been pressed
            ch = msvcrt.getwch()        # Get the pressed character
                        
            if ch in (CR, LF):          # If the character is a carriage return or line feed
                cout << endl            # cout << CR << LF
                return line
            
            elif ch == ET:              # Handling Ctrl+C
                raise KeyboardInterrupt

            elif ch == BS:              # Handle backspace character
                if line:                # If the line is not empty 
                    char = line[-1]     # 
                    line = line[:-1]    # Remove the last character from the line
                    if char == HT:      # Remove Horizonal Tab character
                        cout << BS * TAB_SIZE       # Move the cursor back
                    elif char == SP:                # Remove Space character
                        cout << BS                  # Move the cursor back
                    else:
                        cout << BS << SP            # Clear the last character from the screen
                        cout << BS                  # Move the cursor back
            
            elif ch == HT:
                line += ch
                cout << SP * TAB_SIZE            
            
            else:
                line += ch              # Append the character to the end of the line
                cout << ch
        else:
            time.sleep(DELAY)           # Sleep for a short delay (50 ms) to prevent high CPU usage

    cout << ''.join(
        BS * len(line) + SP * len(line)         # Clear the line if timeout is reached
    ) << endl
                                        
    raise TimeoutError("Timeout occurred.")     # raise TimeoutError if timeout is reached



def unix_input_with_timeout(prompt, timeout):
    cout << prompt              # Print the prompt to the console

    settings = termios.tcgetattr(sys.stdin)
    try:
        tty.setraw(sys.stdin)
        output, _, _ = select.select([sys.stdin], [], [], timeout)
        if output:
            return sys.stdin.readline().rstrip()
        else:
            raise TimeoutError("Timeout occurred.")
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)



def input_with_timeout(prompt: typing.Any = '', /, timeout: typing.Union[int, float, None] = 20.0) -> str:
    """\
    This function prompts the user for input and returns the input if received within the specified `timeout`.
    If the input is not received within the `timeout`, a TimeoutError is raised.

    ### Parameters:
    - prompt (Any): The text to display before waiting for input.
    - timeout (Union[int, float, None]): The maximum time to wait for input. Set to `None` for no `timeout`.

    ### Returns:
    - str: The user input if received within the specified `timeout`.

    ### Raises:
    - TimeoutError: If no input is received within the specified `timeout`.
    - TypeError: If the `timeout` is not an instance of `int`, `float`, or `None`.
    - ValueError: If the `timeout` value is less than or equal to zero.

    ### Usage:
    ```python
        # To get input with a timeout:
        result = input_with_timeout("Please enter your input: ", timeout=15.0)

        # To get input without a timeout:
        result = input_with_timeout("Please enter your input: ", timeout=None)
    """

    if not isinstance(timeout, (int, float, types.NoneType)):
        raise TypeError(f"timeout must be 'int' or 'float' or 'None', not {type(timeout)}.")
    elif timeout is None:
        return builtins.input(prompt)
    elif timeout <= 0:
        raise ValueError(f"timeout value must be greater than zero, timeout: {timeout}.")

    try:
        global msvcrt, time
        import msvcrt, time
        func = windows_input_with_timeout
    
    except ImportError:
        global sys, tty, termios, select
        import sys, tty, termios, select
        func = unix_input_with_timeout

    finally:
        return func(prompt, timeout)

