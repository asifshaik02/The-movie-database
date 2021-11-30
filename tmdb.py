import requests
import json
from urllib.parse import quote



class Tmdb:

    API_KEY = None
    base_url = 'https://api.themoviedb.org/3/'
    img_url = 'https://image.tmdb.org/t/p/w500'

    def __init__(self,key):
        self.API_KEY = key

    # def pretty_print(self,obj):
    #     if type(obj) == dict:
    #         for key in obj:
    #             print(f"{key} : {obj[key]}")

    #     elif type(obj) == list:
    #         for item in obj:
    #             self.pretty_print(item)
        
        # print()
    
    def dict_to_json(self,data,filename):
        with open(f'{filename}.json', 'w') as fp:
            json.dump(data, fp)

    def get_genre_list(self,id_list):
        genre_list = []
        for _id in id_list:
            genre_list.append(self.get_genre(_id))
        return genre_list

    def get_genre(self,_id):
        endpoint = self.base_url + f"genre/{_id}?api_key={self.API_KEY}"
        r = requests.get(endpoint)
        return r.json()

    def get_gender(self,val):
        if val == 1:
            return "Female"
        elif val == 2:
            return "Male"
        else:
            return "Other"

    # _type can be 'movie' or 'tv' or 'person' 
    def search(self,_type,query):
        endpoint = self.base_url + f'search/{_type}?api_key={self.API_KEY}&query={quote(query)}'
        r = requests.get(endpoint)
        d = r.json()
        search_results = []
        for res in d['results']:
            res_dict = {}
            res_dict['id'] = res['id']
            res_dict['path'] = f"/{_type}/{res['id']}"

            try:
                res_dict['title'] = res['title']
            except KeyError:
                res_dict['title'] = res['name']

            if _type != 'person':
                try:
                    res_dict['img'] = self.img_url + res['poster_path']
                except TypeError:
                    res_dict['img'] = '../static/base.jpg'

                try:
                    res_dict['release_date'] = res['release_date']
                except KeyError:
                    res_dict['release_date'] = res['first_air_date'] 
  
                res_dict['plot'] = res['overview']

            else:
                res_dict['popularity'] = res['popularity']
                try:
                    res_dict['img'] = self.img_url + res['profile_path']
                except TypeError:
                    res_dict['img'] = '../static/base.jpg'
            search_results.append(res_dict)
        
        return search_results


    

    def get_cast(self,_type,_id):
        endpoint = self.base_url + f"{_type}/{_id}/credits?api_key={self.API_KEY}"
        r = requests.get(endpoint)
        cast = []
        for item in r.json()['cast']:
            res_dict = {}
            res_dict['id'] = item['id']
            res_dict['title'] = item['name']
            try:
                res_dict['img'] = self.img_url + item['profile_path']
            except TypeError:
                res_dict['img'] = '../static/base.jpg'

            res_dict['path'] = f"/person/{item['id']}"
            cast.append(res_dict)
        return cast
    
    def get_similar(self,_type,_id):
        endpoint = self.base_url + f"{_type}/{_id}/similar?api_key={self.API_KEY}"
        r = requests.get(endpoint)
        similar = []
        for i in r.json()['results']:
            res_dict = {}
            res_dict['id'] = i['id']
            res_dict['path'] = f'/{_type}/{i["id"]}'

            try:
                res_dict['title'] = i['title']
            except KeyError:
                res_dict['title'] = i['name']
            
            try:
                res_dict['img'] = self.img_url + i['poster_path']
            except TypeError:
                res_dict['img'] = '../static/base.jpg'
            
            similar.append(res_dict)
        return similar

    def get_category_list(self,category, _type):
        if category == 'trending':
            endpoint = self.base_url + f'trending/{_type}/day?api_key={self.API_KEY}'
        else:
            endpoint = self.base_url + f"{_type}/{category}?api_key={self.API_KEY}"
        
        r = requests.get(endpoint)
        d = r.json()
        category_list = []

        for i in d['results']:
            res_dict = {}
            res_dict['id'] = i['id']
            res_dict['path'] = f'/{_type}/{i["id"]}'

            try:
                res_dict['title'] = i['title']
            except KeyError:
                res_dict['title'] = i['name']
            
            if _type == 'person':
                try:
                    res_dict['img'] = self.img_url + i['profile_path']
                except TypeError:
                    res_dict['img'] = '../static/base.jpg'
            else:
                try:
                    res_dict['img'] = self.img_url + i['poster_path']
                except TypeError:
                    res_dict['img'] = '../static/base.jpg'


            category_list.append(res_dict)

        return category_list
    
    def get_details(self, _type, _id):
        endpoint = self.base_url + f"{_type}/{_id}?api_key={self.API_KEY}"
        r = requests.get(endpoint)
        d = r.json()
        res_dict = {}
        res_dict['id'] = d['id']
        try:
            res_dict['title'] = d['title']
        except KeyError:
            res_dict['title'] = d['name']

        res_dict['plot'] = d['overview']
        res_dict['path'] = f"/{_type}/{_id}"
        try:
            res_dict['img'] = self.img_url + d['poster_path']
        except TypeError:
            res_dict['img'] = '../static/base.jpg'

        res_dict['rating'] = d['vote_average']
        try:
            res_dict['release_date'] = d['release_date']
        except KeyError:
            res_dict['release_date'] = d['first_air_date']
        try:
            res_dict['runtime'] = d['runtime']
        except KeyError:
            res_dict['runtime'] = d['episode_run_time'][0]

        res_dict['genre'] = [i['name'] for i in d['genres']]

        return res_dict
    


    # def get_movie_details(self,_id):
    #     d = self.get_details('movie',_id)

    #     res_dict={}  
    #     res_dict['id'] = d['id']
    #     res_dict['title'] = d['title']
    #     res_dict['plot'] = d['overview']
    #     res_dict['path'] = f"/movie/{_id}"
    #     try:
    #         res_dict['img'] = self.img_url + d['poster_path']
    #     except TypeError:
    #         res_dict['img'] = '../static/base.jpg'
    #     res_dict['rating'] = d['vote_average']
    #     res_dict['release_date'] = d['release_date']
    #     res_dict['runtime'] = d['runtime']
    #     res_dict['genre'] = [i['name'] for i in d['genres']]


        
    #     return res_dict

    # def get_tv_details(self,_id):
    #     d = self.get_details('tv', _id)
        
    #     res_dict = {}
    #     res_dict['id'] = d['id']
    #     res_dict['title'] = d['name']
    #     res_dict['plot'] = d['overview']
    #     res_dict['path'] = f"/tv/{_id}"
    #     try:
    #         res_dict['img'] = self.img_url + d['poster_path']
    #     except TypeError:
    #         res_dict['img'] = '../static/base.jpg'

    #     res_dict['rating'] = d['vote_average']
    #     res_dict['release_date'] = d['first_air_date']
    #     res_dict['runtime'] = d['episode_run_time'][0] #list
    #     res_dict['genre'] = [i['name'] for i in d['genres']]

        
    #     return res_dict


    def get_known_for(self,query):
        endpoint = self.base_url + f"search/person?api_key={self.API_KEY}&query={quote(query)}"
        r = requests.get(endpoint)
        d = r.json()


        known_for = []

        for i in d['results'][0]['known_for']:
            res_dict = {}
            res_dict['id'] = i['id']
            try:
                res_dict['title'] = i['title']
            except:
                pass
            try:
                res_dict['img'] = self.img_url + i['poster_path']
            except TypeError:
                res_dict['img'] = '../static/base.jpg'
            
            res_dict['path'] = f"/{i['media_type']}/{i['id']}"

            
            known_for.append(res_dict)
        
        return known_for



    def get_person_details(self,_id):
        endpoint = self.base_url + f"person/{_id}?api_key={self.API_KEY}"
        r = requests.get(endpoint)
        d = r.json()

        res_dict = {}
        res_dict['id'] = d['id']
        res_dict['title'] = d['name']
        res_dict['birthday'] = d['birthday']
        res_dict['bio'] = d['biography']
        res_dict['gender'] = self.get_gender(d['gender'])
        res_dict['prof'] = d['known_for_department']
        try:
            res_dict['img'] = self.img_url + d['profile_path']
        except TypeError:
            res_dict['img'] = '../static/base.jpg'
        
        return res_dict


