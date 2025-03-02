import streamlit as st
from simulation import HappyHospitalSimulation
import time  # For preloader delay

st.title("🏥 Hospital Management Simulation")
st.subheader("Type 'quit' or 'stop' at any time to exit.\n", divider="gray")

# Initialize session state only once
if "simulation" not in st.session_state:
    st.session_state.simulation = HappyHospitalSimulation()
    st.session_state.current_scenario = st.session_state.simulation.simulation_agent.provide_scenario()
    st.session_state.responses = []
    st.session_state.user_response = ""  # Initialize only once
    st.session_state.simulation_summary = None  # Store summary report

roles = [
    "Nurse Chen", "Dr. Smith", "Charlie (Hospital Admin)", "Dr. Rodriguez",
    "Head Nurse Thompson", "IT Specialist Linda", "Pharmacist Lee"
]

# Extract role dynamically from scenario text
def extract_role(scenario_text):
    for role in roles:
        if role in scenario_text:
            return role
    return "Director"

if st.session_state.current_scenario:
    role = extract_role(st.session_state.current_scenario)
    st.write(f"### Your Role: **{role}**")
    st.write(f"📜 **Scenario:** {st.session_state.current_scenario}")

    # ✅ Use session state for controlled input
    user_response = st.text_area("📝 Your Response:", key="user_response")

    if st.button("Submit Response"):
        if user_response.strip():
            if user_response.lower() in ["quit", "stop"]:  # ✅ Handle user exit
                with st.spinner("Generating summary report..."):
                    time.sleep(2)  # Simulated processing delay
                    st.session_state.simulation_summary = (
                        st.session_state.simulation.performance_analyzer.generate_final_summary()
                    )
                st.session_state.current_scenario = None  # Stop the scenario loop
                st.rerun()

            else:
                with st.spinner("Processing..."):  # ✅ Preloader added
                    time.sleep(2)  # Simulate processing delay

                st.session_state.simulation.simulation_agent.update_scenario_flow(user_response)
                st.session_state.simulation.performance_analyzer.analyze_response(user_response, st.session_state.current_scenario)
                st.session_state.responses.append(user_response)

                # ✅ Update scenario for next step
                st.session_state.current_scenario = st.session_state.simulation.simulation_agent.provide_scenario()

                # ✅ Reset input box indirectly by removing key & reloading
                del st.session_state["user_response"]  
                st.rerun()  # ✅ Refresh the UI

elif st.session_state.simulation_summary:
    st.write("## 📊 Final Performance Summary")
    st.write(st.session_state.simulation_summary)

    if st.button("Restart Simulation"):
        st.session_state.clear()
        st.rerun()
else:
    st.write("⚠️ No scenario found. Please restart the simulation.")


# # ✅ Show Preloader while processing
# if st.session_state.get("loading", False):
#     with st.spinner("Processing... Please wait ⏳"):
#         time.sleep(2)  # Simulated delay
#         st.session_state.simulation.simulation_agent.update_scenario_flow(user_response)

#         # ✅ Get the next challenge, keeping the role & context
#         new_scenario = st.session_state.simulation.simulation_agent.provide_scenario()
        
#         # ✅ Ensure the challenge stays contextually connected
#         if new_scenario:
#             st.session_state.current_scenario = new_scenario
#             st.session_state.conversation_history.append(new_scenario)

#         # ✅ Reset input & hide preloader
#         del st.session_state["user_response"]
#         st.session_state.loading = False
#         st.rerun()


# elif "simulation_summary" in st.session_state:
#     st.write("## 📊 Final Performance Summary")
#     st.write(st.session_state.simulation_summary)

#     if st.button("Restart Simulation"):
#         st.session_state.clear()
#         st.rerun()
# else:
#     st.write("⚠️ No scenario found. Please restart the simulation.")
