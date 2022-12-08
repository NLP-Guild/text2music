import numpy as np
import json
import numpy as np
import httpx
import time
from sentence_transformers import SentenceTransformer
import requests

MUBERT_TAGS_STRING = 'tribal,action,kids,neo-classic,run 130,pumped,jazz / funk,ethnic,dubtechno,reggae,acid jazz,liquidfunk,funk,witch house,tech house,underground,artists,mystical,disco,sensorium,r&b,agender,psychedelic trance / psytrance,peaceful,run 140,piano,run 160,setting,meditation,christmas,ambient,horror,cinematic,electro house,idm,bass,minimal,underscore,drums,glitchy,beautiful,technology,tribal house,country pop,jazz & funk,documentary,space,classical,valentines,chillstep,experimental,trap,new jack swing,drama,post-rock,tense,corporate,neutral,happy,analog,funky,spiritual,sberzvuk special,chill hop,dramatic,catchy,holidays,fitness 90,optimistic,orchestra,acid techno,energizing,romantic,minimal house,breaks,hyper pop,warm up,dreamy,dark,urban,microfunk,dub,nu disco,vogue,keys,hardcore,aggressive,indie,electro funk,beauty,relaxing,trance,pop,hiphop,soft,acoustic,chillrave / ethno-house,deep techno,angry,dance,fun,dubstep,tropical,latin pop,heroic,world music,inspirational,uplifting,atmosphere,art,epic,advertising,chillout,scary,spooky,slow ballad,saxophone,summer,erotic,jazzy,energy 100,kara mar,xmas,atmospheric,indie pop,hip-hop,yoga,reggaeton,lounge,travel,running,folk,chillrave & ethno-house,detective,darkambient,chill,fantasy,minimal techno,special,night,tropical house,downtempo,lullaby,meditative,upbeat,glitch hop,fitness,neurofunk,sexual,indie rock,future pop,jazz,cyberpunk,melancholic,happy hardcore,family / kids,synths,electric guitar,comedy,psychedelic trance & psytrance,edm,psychedelic rock,calm,zen,bells,podcast,melodic house,ethnic percussion,nature,heavy,bassline,indie dance,techno,drumnbass,synth pop,vaporwave,sad,8-bit,chillgressive,deep,orchestral,futuristic,hardtechno,nostalgic,big room,sci-fi,tutorial,joyful,pads,minimal 170,drill,ethnic 108,amusing,sleepy ambient,psychill,italo disco,lofi,house,acoustic guitar,bassline house,rock,k-pop,synthwave,deep house,electronica,gabber,nightlife,sport & fitness,road trip,celebration,electro,disco house,electronic'
MUBERT_TAGS = np.array(MUBERT_TAGS_STRING.split(','))
MUBERT_LICENSE = "ttmmubertlicense#f0acYBenRcfeFpNT4wpYGaTQIyDI4mJGv5MfIhBFz97NXDwDNFHmMRsBSzmGsJwbTpP1A6i07AXcIeAHo5"
MUBERT_MODE = "loop"
MUBERT_TOKEN = "4951f6428e83172a4f39de05d5b3ab10d58560b8"






def get_mubert_tags_embeddings(w2v_model):
    return w2v_model.encode(MUBERT_TAGS)


def get_pat(email: str):
    r = httpx.post('https://api-b2b.mubert.com/v2/GetServiceAccess',
                   json={
                       "method": "GetServiceAccess",
                       "params": {
                           "email": email,
                           "license": MUBERT_LICENSE,
                           "token": MUBERT_TOKEN,
                           "mode": MUBERT_MODE,
                       }
                   })

    rdata = json.loads(r.text)
    assert rdata['status'] == 1, "probably incorrect e-mail"
    pat = rdata['data']['pat']
    return pat


def find_similar(em, embeddings, method='cosine'):
    scores = []
    for ref in embeddings:
        if method == 'cosine':
            scores.append(1 - np.dot(ref, em) / (np.linalg.norm(ref) * np.linalg.norm(em)))
        if method == 'norm':
            scores.append(np.linalg.norm(ref - em))
    return np.array(scores), np.argsort(scores)


def get_tags_for_prompts(w2v_model, mubert_tags_embeddings, prompts, top_n=3, debug=False):
    prompts_embeddings = w2v_model.encode(prompts)
    ret = []
    for i, pe in enumerate(prompts_embeddings):
        scores, idxs = find_similar(pe, mubert_tags_embeddings)
        top_tags = MUBERT_TAGS[idxs[:top_n]]
        top_prob = 1 - scores[idxs[:top_n]]
        if debug:
            print(f"Prompt: {prompts[i]}\nTags: {', '.join(top_tags)}\nScores: {top_prob}\n\n\n")
        ret.append((prompts[i], list(top_tags)))
    return ret





minilm = SentenceTransformer('all-MiniLM-L6-v2')
mubert_tags_embeddings = get_mubert_tags_embeddings(minilm)


def get_track_by_tags(tags, pat, duration, maxit=20, loop=False):
    if loop:
        mode = "loop"
    else:
        mode = "track"
    r = httpx.post('https://api-b2b.mubert.com/v2/RecordTrackTTM',
                   json={
                       "method": "RecordTrackTTM",
                       "params": {
                           "pat": pat,
                           "duration": duration,
                           "tags": tags,
                           "mode": mode
                       }
                   })

    rdata = json.loads(r.text)
    assert rdata['status'] == 1, rdata['error']['text']
    trackurl = rdata['data']['tasks'][0]['download_link']

    for i in range(maxit):
        r = httpx.get(trackurl)
        if r.status_code == 200:
            return trackurl
        time.sleep(1)


def generate_track_by_prompt(prompt, duration, loop=False):
    try:
        pat = get_pat('email@example.com')
        _, tags = get_tags_for_prompts(minilm, mubert_tags_embeddings, [prompt, ])[0]
        return get_track_by_tags(tags, pat, int(duration), loop=loop), "Success", ",".join(tags)
    except Exception as e:
        return None, str(e), ""


def generate_and_store(prompt,duration,output_path: str,loop=False,):
    url, state, tags = generate_track_by_prompt(prompt,duration,loop)
    r = requests.get(url, allow_redirects=True)

    open(f'{output_path}.mp3', 'wb').write(r.content)

