import streamlit as st
import time

# Set the refresh interval in milliseconds
refresh_interval = 10 * 1000  # 10 seconds

# Inject JavaScript to auto-refresh the page
refresh_script = f"""
<script>
    setInterval(function() {{
        window.location.reload();
    }}, {refresh_interval});
</script>
"""

# Inject the JavaScript into the Streamlit app
st.markdown(refresh_script, unsafe_allow_html=True)

# Streamlit content
st.title("Auto-Refreshing Streamlit Application")

# Display the current time
current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
st.write(f"The current time is: {current_time}")

# Add some interactive content
if st.button("Click me!"):
    st.write("Button clicked!")

st.write("This page will automatically refresh every 10 seconds.")
