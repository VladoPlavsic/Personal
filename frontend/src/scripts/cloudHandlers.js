import EasyYandexS3 from 'easy-yandex-s3'

export function getCloudClient(){
    return new EasyYandexS3({
        auth:{
            accessKeyId: process.env.VUE_APP_ACCESS_KEY_ID,
            secretAccessKey: process.env.VUE_APP_SECRET_ACCESS_KEY,
        },
        Bucket: 'vlado',
    })
}