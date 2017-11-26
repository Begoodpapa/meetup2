import React , { Component } from 'react';
import ReactDOM from 'react-dom';

export class FormEdit extends Component{
    constructor(props){
      super(props)
      this.state = {
        edit: false,
        content: "",
      }

      const {onFinish} = this.props
      this.onFinish = onFinish
      this.finish = this.finish.bind(this)
    }

    finish(evt){
      this.onFinish(this.state.content)
      evt.preventDefault()
      evt.stopPropagation()
      this.changeEdit()
    }

    edit(evt){
      this.setState({content: evt.target.value})
    }

    changeEdit(){
      const {val} = this.props
      if (!this.state.edit){
        this.setState({content: val })
      }
      this.setState({edit: !this.state.edit})
    }


    render(){
      const {val, placeholder, type} = this.props

      if (this.state.edit){
        return (
         <form
           onSubmit={this.finish.bind(this)}>
           {
             (type == "textarea")?(
               <textarea type="text" 
                 className="form-control" 
                 placeholder={placeholder}
                 onBlur={this.finish.bind(this)}
                 onChange={this.edit.bind(this)}  
                 value={this.state.content}/>

             ):(
               <input type="text" 
                 className="form-control" 
                 placeholder={placeholder}
                 onBlur={this.finish.bind(this)}
                 onChange={this.edit.bind(this)}  
                 value={this.state.content}/>
             )
           }
           {type=="textarea"?<button className="bg-btn bg-btn--default" onClick={this.finish.bind(this)}> 提交</button>:null}
         </form>)
      }else{
        if(type=="textarea"){
         return <pre onClick={this.changeEdit.bind(this)}>{(val&&val.length>0)?val: placeholder}</pre>
        }else{
         return <span onClick={this.changeEdit.bind(this)}>{(val&&val.length>0)?val: placeholder}</span>
        }
      }
    }
}
