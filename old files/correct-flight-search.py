import os
import json
import requests
from typing import Dict, Any, List
from dotenv import load_dotenv

class FlightSearchAssistant:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
            
        self.base_url = 'https://api.anthropic.com/v1/messages'
        # Correct headers including the beta flag
        self.headers = {
            'content-type': 'application/json',
            'x-api-key': self.api_key,
            'anthropic-version': '2023-06-01',
            'anthropic-beta': 'computer-use-2024-10-22'
        }

    def run_search(self, departure_city: str, start_date: str, end_date: str) -> None:
        prompt = f"""
        Help me find flight destinations from {departure_city} between {start_date} and {end_date}.
        
        Please follow these steps:
        1. Navigate to flights.google.com in the browser
        2. Enter {departure_city} as the departure city
        3. Leave the destination blank
        4. Set the departure date to {start_date} and return date to {end_date}
        5. Wait for the results to load
        6. Sort by price if possible
        7. Take a screenshot of the results
        8. Analyze the visible results and recommend the top 5 cheapest destinations

        After each step, take a screenshot and carefully evaluate if you have achieved the right outcome.
        Explicitly show your thinking: "I have evaluated step X..." If not correct, try again.
        Only when you confirm a step was executed correctly should you move on to the next one.
        """

        messages = [{"role": "user", "content": prompt}]
        
        while True:
            try:
                # Make request to Claude with all required tools
                response = requests.post(
                    self.base_url,
                    headers=self.headers,
                    json={
                        'model': 'claude-3-5-sonnet-20241022',
                        'max_tokens': 1024,
                        'tools': [
                            {
                                'type': 'computer_20241022',
                                'name': 'computer',
                                'display_width_px': 1024,
                                'display_height_px': 768,
                                'display_number': 1
                            },
                            {
                                'type': 'text_editor_20241022',
                                'name': 'str_replace_editor'
                            },
                            {
                                'type': 'bash_20241022',
                                'name': 'bash'
                            }
                        ],
                        'messages': messages
                    }
                )
                response.raise_for_status()
                result = response.json()
                
                # Print Claude's thoughts/analysis
                if result.get('content'):
                    print(result['content'])

                # Check for tool use
                if result.get('stop_reason') == 'tool_use':
                    tool_calls = result.get('tool_calls', [])
                    for tool_call in tool_calls:
                        # Get details about the tool call
                        tool_name = tool_call.get('name')
                        tool_input = tool_call.get('parameters', {})
                        
                        print(f"\nExecuting {tool_name}...")
                        print(f"Input: {json.dumps(tool_input, indent=2)}")
                        
                        # Here your application would:
                        # 1. Execute the tool in your environment
                        # 2. Get the results
                        # 3. Format them according to the tool's expected response format
                        
                        # For now, we'll just acknowledge receipt
                        print("Tool execution would happen here")
                        
                        # Add to message history
                        messages.extend([
                            {
                                "role": "assistant",
                                "content": result.get('content', ''),
                                "tool_calls": [tool_call]
                            },
                            {
                                "role": "tool",
                                "tool_call_id": tool_call.get('id'),
                                "name": tool_name,
                                "content": json.dumps({
                                    "type": "success",
                                    "message": "Tool execution acknowledged"
                                })
                            }
                        ])
                else:
                    # Claude is done
                    break
                    
            except requests.exceptions.RequestException as e:
                print(f"Error communicating with Claude: {e}")
                break

def main():
    try:
        # departure_city = input("Enter departure city: ")
        # start_date = input("Enter start date (YYYY-MM-DD): ")
        # end_date = input("Enter end date (YYYY-MM-DD): ")

        print("\nStarting flight search...\n")
        
        assistant = FlightSearchAssistant()
        # assistant.run_search(departure_city, start_date, end_date)
        assistant.run_search("Austin", "2024-12-01", "2024-12-08")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
