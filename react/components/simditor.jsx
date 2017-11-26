'use strict';
import React from 'react';
import Simditor from "simditor";
import $ from "jquery";
import BASE_URL from 'config';
//import {ENV} from '../common/url';

require("../../node_modules/simditor/styles/simditor.css");

/**
 * 取值 let goods_desc = $(".detailContainer").find(".simditor-body").html();
 */

class SimditorTextarea extends React.Component {

    componentDidMount = () => {
      this.initEditor();
      // $(".font-color.font-color-default").removeClass("font-color-default").addClass("font-color-8");
    };

    initEditor = () => {
        let config = {
            placeholder: this.props.placeholder,
            defaultImage: 'images/image.png',
            params: {},
            tabIndent: true,
            toolbar: [
                'title',
                'bold',
                'italic',
                'underline',
                'strikethrough',
                'fontScale',
                'color',
                'link',
                'hr',
                'image',
                'indent',
                'outdent',
                'alignment',
            ],
            upload: {
                url: BASE_URL + 'group/uploadimage', //文件上传的接口地址
                params: {
                    groupID: '50',
                    dir: 'y',
                    hash: '',
                }, //键值对,指定文件上传接口的额外参数,上传的时候随文件一起提交
                                
                fileKey: 'file', //服务器端获取文件数据的参数名
                connectionCount: 3,
                leaveConfirm: '正在上传文件',
            },

            toolbarFloat: true,
            toolbarFloatOffset: 0,
            toolbarHidden: false,
            pasteImage: false,
            cleanPaste: false,
            textarea: $(this.refs.textarea)
        };

        this.editor = new Simditor(config);// 初始化编辑器
        this.editor.setValue(this.props.value);

        //监听改变        
        this.editor.on("valuechanged", (e, src) => {
        	
          this.props.onChange(this.getValue());
        });        

        //更改图片上传类型
        $(".simditor input[type='file']").attr('accept', 'image/jpg,image/jpeg,image/png,image/bmp');
    };

    componentWillReceiveProps(nextProps){    
      this.editor.setValue(nextProps.value);
    };

    getValue = () => {
      return this.editor.getValue().trim();
      //let selectName = '#${this.props.id}.simditor';
      
      //let html = $(selectName).find(".simditor-body").html();
      //let html = $(".simditor").find(".simditor-body").html();
      //console.log("html is:"+html);
      //return html;
    };

    render() {
      return (
          <textarea
              id={this.props.id}
              ref="textarea"
              placeholder="请输入内容"/>
      );
    }
}

export default SimditorTextarea;