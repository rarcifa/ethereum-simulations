from cronos_chain_client import create_client

client = create_client({
    'chain': 'evm',
    'network': 'mainnet',
    'explorer': {
        'apiKey': 'OPPTIONAL_API_KEY', # Optional
    }
})

tokens = client.tokens.getCRC20TokenList()
print(tokens)