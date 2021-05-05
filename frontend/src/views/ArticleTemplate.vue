<template>
    <div>
        <Header v-on="$listeners" firstSelect="About" secondSelect="Contact" thirdSelect="Articles" firstSelectHref="/about" secondSelectHref="/contact" thirdSelectHref="/articles"/>
    
        <div v-if="$cookies.loggedIn === 'true'">
            <div id="body">
                <div id="articlePicker" >
                    <div class="items">
                        <div class="items-head">
                            <p>{{$route.params.name}}</p>
                            <hr>
                        </div>
                        
                        <div class="items-body" v-for="(article, i) in previewData" :key="i">
                            <div class="items-body-content" :id="article.id" v-on:click="changeArticle">
                                <span :id="article.id">{{article.name}}</span>
                                <i v-if="$parent.edit" v-on:click="deleteArticle" :id="article.id">X</i>
                            </div>
                        </div>
                    </div>
                </div>

                <div id="center">
                    <div id="article" v-if="!$parent.edit">
                        <div id="articleTitle">
                            <h2 v-html="articleData.name">{{articleData.name}}</h2>
                        </div>
                        <div v-html="articleData.content" id="articleBody">
                        </div>
                        <div id="articleSignature">
                            {{articleData.author}}
                        </div>
                    </div>
                    <div v-else id="articleEditing">
                        <div id="articleTitle">
                            <h2>{{editorData.name}}</h2>
                        </div>
                        <div v-html="editorData.content" id="articleBody">
                        </div>
                        <div id="articleSignature">
                            {{editorData.author}}
                        </div>
                    </div>
                    <!--Edit-->
                    <div id="editor" v-if="$parent.edit"> 
                        Article title:
                        <textarea id="articleTitle" v-model.trim="editorData.name" placeholder="Title"></textarea>
                        <p></p>
                        Article:
                        <ckeditor :editor="editor" v-model.trim="editorData.content" :config="editorConfig"></ckeditor>
                        <p></p>
                        Author:
                        <textarea id="articleSignature" v-model.trim="editorData.author" placeholder="Signature"></textarea>
                        <p></p>
                        <div id="editButtons">
                            <button v-on:click="updateArticle">Update</button>
                            <button v-on:click="insertArticle">Insert</button>
                            <button v-on:click="clearFields">Reset</button>
                        </div>  
                    </div>
                </div>
            
                 <!-- Ghost div for aligning -->
                <div>
                </div>
            </div>
            
           
        </div>
        <div  v-if="$cookies.loggedIn === 'false'" class="body">
            <div id="body">
                <div id="accessDenied">
                    <a href="/sign/in">Access denied!</a>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import Header from '@/components/Header'
//import ClassicEditor from '@ckeditor/ckeditor5-build-classic';

import axios from 'axios'
import { raiseError, raiseAllertDelete } from '../scripts/allertHandlers'

import ClassicEditor from '@ckeditor/ckeditor5-editor-classic/src/classiceditor.js';
import Alignment from '@ckeditor/ckeditor5-alignment/src/alignment.js';
import Autoformat from '@ckeditor/ckeditor5-autoformat/src/autoformat.js';
import Autolink from '@ckeditor/ckeditor5-link/src/autolink.js';
import BlockQuote from '@ckeditor/ckeditor5-block-quote/src/blockquote.js';
import Bold from '@ckeditor/ckeditor5-basic-styles/src/bold.js';
import CKFinderUploadAdapter from '@ckeditor/ckeditor5-adapter-ckfinder/src/uploadadapter.js';
import CloudServices from '@ckeditor/ckeditor5-cloud-services/src/cloudservices.js';
import Essentials from '@ckeditor/ckeditor5-essentials/src/essentials.js';
import FontColor from '@ckeditor/ckeditor5-font/src/fontcolor.js';
import FontFamily from '@ckeditor/ckeditor5-font/src/fontfamily.js';
import FontSize from '@ckeditor/ckeditor5-font/src/fontsize.js';
import Heading from '@ckeditor/ckeditor5-heading/src/heading.js';
import Indent from '@ckeditor/ckeditor5-indent/src/indent.js';
import Italic from '@ckeditor/ckeditor5-basic-styles/src/italic.js';
import Link from '@ckeditor/ckeditor5-link/src/link.js';
import List from '@ckeditor/ckeditor5-list/src/list.js';
import MediaEmbed from '@ckeditor/ckeditor5-media-embed/src/mediaembed.js';
import Paragraph from '@ckeditor/ckeditor5-paragraph/src/paragraph.js';
import PasteFromOffice from '@ckeditor/ckeditor5-paste-from-office/src/pastefromoffice';
import Table from '@ckeditor/ckeditor5-table/src/table.js';
import TableCellProperties from '@ckeditor/ckeditor5-table/src/tablecellproperties';
import TableProperties from '@ckeditor/ckeditor5-table/src/tableproperties';
import TableToolbar from '@ckeditor/ckeditor5-table/src/tabletoolbar.js';
import TextTransformation from '@ckeditor/ckeditor5-typing/src/texttransformation.js';
import Underline from '@ckeditor/ckeditor5-basic-styles/src/underline.js';
import CodeBlock from '@ckeditor/ckeditor5-code-block/src/codeblock.js'

export default {
    name: 'ArticleTemplate',
    data() {
        return{
            editor: ClassicEditor,
            editorData: {
                content: '',
                name: '',
                author: '',
                id: -1,
            },
            editorConfig: {
                plugins: [
                        Alignment,
                        Autoformat,
                        Autolink,
                        BlockQuote,
                        Bold,
                        CKFinderUploadAdapter,
                        CloudServices,
                        Essentials,
                        FontColor,
                        FontFamily,
                        FontSize,
                        Heading,
                        Indent,
                        Italic,
                        Link,
                        List,
                        MediaEmbed,
                        Paragraph,
                        PasteFromOffice,
                        Table,
                        TableCellProperties,
                        TableProperties,
                        TableToolbar,
                        TextTransformation,
                        Underline,
                        CodeBlock,
                    ],

                    toolbar: {
                        items: [
                               "heading",
                                "|",
                                "bold",
                                "italic",
                                "link",
                                "bulletedList",
                                "numberedList",
                                "|",
                                "outdent",
                                "indent",
                                "codeBlock",
                                "|",
                                "blockQuote",
                                "insertTable",
                                "mediaEmbed",
                                "undo",
                                "redo",
                                "alignment",
                                "underline",
                                "fontColor",
                                "fontSize",
                                "fontFamily",

                        ]
                    },
                    image: {
                        toolbar: ["imageTextAlternative", "imageStyle:full", "imageStyle:side"],
                    },
                    table: {
                        contentToolbar: [
                        "tableColumn",
                        "tableRow",
                        "mergeTableCells",
                        "tableCellProperties",
                        "table"
                        ]
                    }
            },
            subgroupId: -1,
            articleData:{},
            previewData: []
        }
    },
    beforeCreate(){
        // get id of current subcategory
        axios.get(process.env.VUE_APP_REST_API_IP + "/api/articles/get/subgroup/id?url=articles/" + this.$route.params.name
        ).then((response) => {
            this.subgroupId = response.data;
            // get all articles in this subcategory (preview only)
            axios.get(process.env.VUE_APP_REST_API_IP + "/api/articles/get/articles/preview?group_fk=" + this.subgroupId
            ).then((response) => {
                this.previewData = response.data;
                // get first article and show it
                axios.get(process.env.VUE_APP_REST_API_IP + "/api/articles/get/article?id=" + this.previewData[0].id
                ).then((response) =>{
                    this.articleData = response.data;
                }).catch((error) => {

                });

            }).catch((error) => {

            });
        });

      
    },
    methods: {
        insertArticle(){
            var existingArticles = this.previewData.filter(articles => articles.name.toLowerCase());

            if (!this.editorData.name){
                raiseError("Title can't be empty!");
                return;
            }else if(existingArticles.includes(this.editorData.name.toLowerCase())){
                raiseError("Article with this name already exists in category: " + this.$route.params.name);
                return;
            }else if (!this.editorData.author){
                raiseError("Author can't be empty!");
                return;
            }else if(!this.editorData.content){
                raiseError("Content can't be empty!");
                return;
            }

            axios.post(process.env.VUE_APP_REST_API_IP  + "/api/articles/create/article?token=" + this.$cookies.jwt, {
                new_article: {
                    name: this.editorData.name.replace(/'/g,"`"),
                    content: this.editorData.content.replace(/'/g,"`"),
                    author: this.editorData.author.replace(/'/g,"`"),
                    group_fk: this.subgroupId,
                }
            }).then((response) => {
                this.updateData();
            }).catch((error) => {
                console.log(error);
            })
        },
        updateArticle(){
            var existingArticles = this.previewData.filter(articles => articles.name.toLowerCase() != this.editorData.name.toLowerCase());

            if (!this.editorData.name){
                raiseError("Title can't be empty!");
                return;
            }else if(existingArticles.includes(this.editorData.name.toLowerCase())){
                raiseError("Article with this name already exists in category: " + this.$route.params.name);
                return;
            }else if (!this.editorData.author){
                raiseError("Author can't be empty!");
                return;
            }else if(!this.editorData.content){
                raiseError("Content can't be empty!");
                return;
            }

            axios.put(process.env.VUE_APP_REST_API_IP + "/api/articles/update/article?token=" + this.$cookies.jwt, {
                updated_article: {
                    id: this.editorData.id,
                    name: this.editorData.name.replace(/'/g,"`"),
                    content: this.editorData.content.replace(/'/g,"`"),
                    author: this.editorData.author.replace(/'/g,"`")
                }
            }).then((response) => {
                this.updateData();
            })

        },
        deleteArticle(e){
            var id = e.target.id;
            var deletingArticle = this.previewData.filter(article => article.id == id)[0];
            raiseAllertDelete("You are about to delete: " + deletingArticle.name).then((response) => {
                if(response){
                    
                    axios.delete(process.env.VUE_APP_REST_API_IP + "/api/articles/delete/article?id=" + id + "&token=" + this.$cookies.jwt
                    ).then((response) => {
                        this.updateData();
                    }).catch((error) => {})

                }
            })

        },
        changeArticle(e){

            // load new data
            axios.get(process.env.VUE_APP_REST_API_IP + "/api/articles/get/article?id=" + e.target.id
                ).then((response) =>{
                    this.articleData = response.data;
                    if(this.$parent.edit){
                        this.editorData.id = this.articleData.id;
                        this.editorData.name = this.articleData.name;
                        this.editorData.author = this.articleData.author;
                        this.editorData.content = this.articleData.content;
                    }else{
                        this.editorData = {
                            id: -1,
                            name: '',
                            author: '',
                            content: '',
                        };
                    }

                }).catch((error) => {

            });
        },
        updateData(){
            // get new preview data
            axios.get(process.env.VUE_APP_REST_API_IP + "/api/articles/get/articles/preview?group_fk=" + this.subgroupId
            ).then((response) => {
                this.previewData = response.data;
                // get first article and show it
                axios.get(process.env.VUE_APP_REST_API_IP + "/api/articles/get/article?id=" + this.previewData[0].id
                ).then((response) =>{
                    this.articleData = response.data;
                }).catch((error) => {});
            }).catch((error) => {});
        },
        clearFields(){
            this.editorData = {}; 
        },
    },
    components: {
        Header,
    },
     
}
</script>


<style scoped>
#accessDenied{
    position: absolute;
    right: 47vw;
    bottom: 48vh;
}

#body{
    margin-left: 10px;
    margin-right: 10px;
    border-top: 5px solid black;
    padding-top: 5vh;
    display: flex;
    margin-top: 5vh;
    justify-content: space-between;
    flex-direction: row;
}

#articlePicker{
    display: flex;
    flex-direction: column;
}

#articleChoices {
    margin-top: 10px;
}

#article{
    padding-bottom: 10px;
    border-bottom: 2px solid black;
    margin-bottom: 20px;
}

#articleEditing{
    padding-bottom: 10px;
    margin-bottom: 40px;
    border-bottom: 2px solid black;
}

#articleSignature{
    display: flex;
    justify-content: flex-end;
}

#articleTitle{
    display: flex;
    justify-content: center;
}


#editor{
  display: flex;
  flex-direction: column;
  min-height: 200px;
  justify-content: center;
}

#center{
  display: flex;
  flex-direction: column;
  align-self: center;
  justify-content: center;
}


.items {
  width: 300px;
  background: transparent;
  box-shadow: 0 3px 6px rgba(black,0.16), 0 3px 6px rgba(black,0.23);
}

.items-head p{
  padding: 5px 20px;
  margin: 10px;
  color: #0B5AA2;
  font-weight: bold;
  font-size: 20px;
}

.items-head hr {
  width: 20%;
  margin: 0px 30px;
  border: 1px solid rgb(180, 180, 1);
}

.items-body {
  padding: 10px;
  margin: 10px;
  display: grid;
  grid-gap: 10px;
}

.items-body-content {
  padding: 10px;
  padding-right: 0px;
  display: grid;
  grid-template-columns: 10fr 1fr;
  font-size: 13px;
  grid-gap: 10px;
  border: 1px solid transparent;
  cursor: pointer;
  
}

.items-body-content:hover {
  border-radius: 15px;
  border: 1px solid green;
}

.items-body-content i {
  align-self: center;
  font-size: 15px;
  color: green;
  font-weight: bold;
  animation: icon 1.5s infinite forwards;
}

@keyframes icon {
  0%,100%{
    transform: translate(0px);
  }
  50% {
    transform: translate(3px);
  }
}

@media only screen and (max-width: 1000px) {

    #body{
        flex-direction: column;
        flex-wrap: wrap;
    }

    #center{
        margin-top: 20px;
        flex-wrap: wrap;
        border-top: 1px solid black;
    }

}
</style>
