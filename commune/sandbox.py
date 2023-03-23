
import commune

# you can create a key from any string
key = commune.key(seed_hex='alice')
key_class = key.__class__

# or you can generate it from a mnemonic
mnemonic =  key_class.generate_mnemonic()
key2 = commune.key(mnemonic=mnemonic)

# if nothing is provided, a random key is generated (using the mnemonic method)
key3 = commune.key()

# verify that the key is the same as the signture

data_list = [{'bro': 'bro'}, 'whadup']
import streamlit as st
for data in data_list:
    
    signature : dict = key.sign(data=data, return_dict=True)
    
    
    # verifity the signature
    assert key.verify(signature) == True

    # if we switch the public_key the verification will fail
    signature['public_key'] = key2.public_key
    assert key.verify(signature) == False

st.write(key3.params)
key2.set_params(**key3.params)
st.write(key2.params)


