from flask import Flask, render_template, request
import hashlib as hasher
from validate import validate
app = Flask(__name__)

@app.route('/',methods = ['GET'])
def student():
    return render_template('submit_block.html', result = blockchain)

@app.route('/blockchain',methods = ['POST', 'GET'])
def blockchain():
    if request.method == 'POST':
        result = request.form
        previous_block = blockchain[-1]
        if validate(result['Nonse'], previous_block.hash):
            hashed_name = hasher.sha256(result['Name'].encode('utf-8')).hexdigest()
            if hashed_name in leaderboard.keys():
                leaderboard[hashed_name] += 1
            else:
                leaderboard[hashed_name] = 1
            blockchain.append(Block(hashed_name, previous_block.hash))
        return render_template("blockchain.html", result = convert_to_string(blockchain), lead = leaderboard_to_string(leaderboard))
    else:
        return render_template("blockchain.html", result = convert_to_string(blockchain), lead = leaderboard_to_string(leaderboard))

class Block:
    def __init__(self, data, previous_hash):
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.hash_block()

    def hash_block(self):
        string = str(self.data) + str(self.previous_hash)
        return hasher.sha256(string.encode('utf-8')).hexdigest()

    def get_hash(self):
        return self.hash

    def get_data(self):
        return self.data


def genesis_block():
    return Block("Genesis Block", "0")

blockchain = [genesis_block()]
leaderboard = {}

def convert_to_string(blockchain):
    # Take dict and convert to string for output
    string = []
    for i, block in enumerate(blockchain):
        if i == 0:
            string.append(['NAME', 'MINER', 'HASH'])
            string.append([i, 'GENESIS BLOCK', block.hash])
        else:
            string.append([i, block.data, block.hash])
    return string

def leaderboard_to_string(leaderboard):
    string = []
    string.append(['MINER', 'BLOCKS'])
    for key in leaderboard:
        string.append([key, leaderboard[key]])
    return string

if __name__ == '__main__':
   app.run(debug = True, host = '0.0.0.0')
