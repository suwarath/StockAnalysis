from flask import Flask, request, jsonify

from model_element.preprocess import *
from model_element.model import *
    
def load_and_get_action(json_data):
    ticker = json_data['ticker']
    target_date = json_data['target_date']
    date = dt.datetime.strptime(target_date, "%Y-%m-%d")
    start_date = (date - dt.timedelta(days=60)).strftime('%Y-%m-%d')
    end_date = (date + dt.timedelta(days=1)).strftime('%Y-%m-%d')
    data = yf.download(ticker, start=start_date, end=end_date).reset_index()
    data['macd'] = MACD(data['Close']).macd()
    data['macd_signal'] = MACD(data['Close']).macd_signal()
    data['macd_diff'] = MACD(data['Close']).macd_diff()
    data['obv'] = calculate_obv(data)
    target_date_data = data[data['Date'] == target_date].reset_index(drop = True)

    if len(target_date_data) == 0:
        msg = "Market is close"
        return msg, msg, msg, msg
    
    state = np.array([target_date_data.loc[0,i] for i in parameters])

    env_end = date.strftime('%Y-%m-%d')
    env_start = (date - dt.timedelta(days = 365)).strftime('%Y-%m-%d')
    env = StockTradingEnv(ticker, env_start, env_end)
    agent = QLearningAgent(env)
    
    with open('./model_element/qtable.bin', 'rb') as file:
        agent.q_table = pickle.load(file)

    action = agent.choose_action(state)
    action_mapping = {0: 'Sell', 1: 'Hold', 2: 'Buy'}
    
    parm_dict = {}
    for i in parameters:
        parm_dict[i] = target_date_data.loc[0,i]
    
    return target_date, action_mapping[action], state, parm_dict 

app = Flask('get_trade_action')

@app.route('/get_action', methods=['POST'])
def get_action_endpoint():
    ticker_info = request.get_json()

    target_date, action, state, parm_dict = load_and_get_action(ticker_info)

    result = {
        'target_date': target_date,
        'action': action,
        'parm_dict': str(parm_dict)
    }

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, host= "0.0.0.0", port = "9696")
