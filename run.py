from flusso.option import Some
import sys

sys.path.append('.')


# Create an OptionMonad instance with a value
opt = Some(42)

# Map a function over the instance
new_opt = opt.map_(lambda x: x * 2)

# Unwrap the value from the instance
result = new_opt.unwrap()

print(result)  # Output: 84
