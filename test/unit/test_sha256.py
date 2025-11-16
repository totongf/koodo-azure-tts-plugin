import hashlib


def calculate_sha256(text):
    """计算文本的SHA256哈希值"""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# 使用示例
script = """const getAudioPath=async(t,e,i,n)=>{const path=require(\"path\"),fs=require(\"fs\");let filename=new Date().getTime()+\".wav\",outputPath=path.join(i,\"tts\");return fs.existsSync(outputPath)||fs.mkdirSync(outputPath,{recursive:!0}),getTTSAudio(t,e,n).then(audioData=>{let filePath=path.join(outputPath,filename);return fs.writeFileSync(filePath,audioData),filePath}).catch(error=>{throw console.error(\"生成音频失败:\",error),error})},objectToQueryString=obj=>{let params=[];for(const key in obj)if(obj.hasOwnProperty(key)){let value=obj[key],encodedKey=encodeURIComponent(key),encodedValue=encodeURIComponent(value);params.push(`${encodedKey}=${encodedValue}`)}return params.join(\"&\")},getTTSAudio=async(t,e,n)=>{const axios=require(\"axios\");let url=n.url||\"http://127.0.0.1:5003/api/tts\",voice=n.voice||\"xiaoxiao\",token=n.token||\"azure-tts-2024\",params={text:t,voice:voice,e:e.toString(),token:token},queryString=objectToQueryString(params),fullUrl=`${url}?${queryString}`;return new Promise((resolve,reject)=>{axios.get(fullUrl,{responseType:\"arraybuffer\",timeout:3e4}).then(response=>(console.log(\"Azure TTS 请求成功\"),resolve(response.data))).catch(error=>{let errorMessage=\"音频生成失败\";error.response?(errorMessage=`服务器错误: ${error.response.status}`,error.response.data&&(()=>{try{let errorText=Buffer.from(error.response.data).toString('utf8');errorMessage+=` - ${errorText}`}catch(e){}})()):error.request?errorMessage=\"网络连接失败\":errorMessage=error.message,console.error(errorMessage),reject(new Error(errorMessage))})})};global.getAudioPath=getAudioPath;"""

hash_value = calculate_sha256(script)
print(f"SHA256哈希值: {hash_value}")
