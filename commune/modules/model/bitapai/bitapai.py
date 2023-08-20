import http.client
import json
import commune as c




class BitAPAI(c.Module):
    def __init__(self,  config=None,  **kwargs):
        config = self.set_config(config=config, kwargs=kwargs)
        self.conn = http.client.HTTPSConnection(self.config.host)
        self.set_api_key(api_key=config.api_key)
        
    def set_api_key(self, api_key:str):
        assert isinstance(api_key, str)
        if api_key == None:
            api_key = self.get_api_key(api_key)
        
        self.api_key = api_key
        c.print(self.api_key)
            
    
    def forward( self, 
                text:str ,
                # api default is 20, I would not go less than 10 with current network conditions
                # larger number = higher query spread across top miners but slightly longer query time
                 count:int = 5,
                 # changed to False, I assume you only want a single repsonse so it will return a single random from the pool of valid responses
                 return_all:bool = False,
                 # added exclude_unavailable to ensure no empty responses are returned
                 exclude_unavailable:bool = True,
                 uids: list = None,
                 api_key:str = None, history:list=None) -> str: 
        api_key = api_key if api_key != None else self.api_key
        # build payload


        payload =  {
            'messages': 
                    [
                    {
                        "role": "system",
                        "content": "You are an AI assistant"
                    },
                    {
                        "role": "user",
                        "content": text
                    }
                    ],
            "count": count,
            "return_all": return_all,
            # added return all here
            "exclude_unavailable": exclude_unavailable

        }
        if uids is not None:
            payload['uids'] = uids

        if history is not None:
            assert isinstance(history, list)
            assert len(history) > 0
            assert all([isinstance(i, dict) for i in history])
            payload = payload[:1] +  history + payload[1:]


        payload = json.dumps(payload)
        headers = {
        'Content-Type': 'application/json',
        'X-API-KEY': api_key
        }

        
        self.conn.request("POST", "/text", payload, headers)


        res = self.conn.getresponse()
        data = res.read().decode("utf-8")
        c.print(data)
        data = json.loads(data)
        if 'assistant' not in data:
            return data
        return data['assistant']['messages'][0]['content']
    
    
    talk = generate = forward
    
    def test(self):
        return self.forward("hello")


    ## API MANAGEMENT ##

    @classmethod
    def add_api_key(cls, api_key:str):
        assert isinstance(api_key, str)
        api_keys = cls.get('api_keys', [])
        api_keys.append(api_key)
        api_keys = list(set(api_keys))
        cls.put('api_keys', api_keys)
        return {'api_keys': api_keys}


    @classmethod
    def rm_api_key(cls, api_key:str):
        assert isinstance(api_key, str)
        api_keys = cls.get('api_keys', [])
        for i in range(len(api_keys)):
            if api_key == api_keys[i]:
                api_keys.pop(i)
                break   

        cls.put('api_keys', api_keys)
        return {'api_keys': api_keys}


    @classmethod
    def get_api_key(cls):
        api_keys = cls.get('api_keys', [])
        if len(api_keys) == 0:
            return None
        else:
            return c.choice(api_keys)

    @classmethod
    def api_keys(cls):
        return cls.get('api_keys', [])

 