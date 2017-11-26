var React = require('react');
import { Component} from 'react'
import { render } from 'react-dom';
import  {FormEdit} from './form.jsx'
var classNames = require('classnames');
import axios from 'axios'; var qs = require('qs');


class ChoiceEdit extends Component{
    constructor(props){
      super(props)
      this.state = {
        edit: false,
        content: "",
      }

      const {onFinish, } = this.props
      this.onFinish = onFinish
      this.finish = this.finish.bind(this)
    }

    componentWillReceiveProps(newProps){
      this.setState({content: newProps.val})
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
      const {val, placeholder, type, onDelete, onMoveUp, onMoveDown} = this.props

      if (this.state.edit){
        return (
         <div
            className ='survey-choice-edit' >
           <form
             onSubmit={this.finish.bind(this)}> {
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
           </form>
           <div className="survey-choice-edit__control">
           <ul>
             <li>
               <button className='btn btn-default' onClick={()=>{
                 //this.setState({edit: false}) //why????
                 onDelete()
               }}>delete</button>
             </li>
             <li>
               <button className='btn btn-default' onClick={()=>{
                 //this.setState({edit: false})
                 onMoveUp()
               }}>up</button>
             </li>
             <li>
               <button className='btn btn-default' onClick={()=>{
                 //this.setState({edit: false})
                 onMoveDown()
               }}>down</button>
             </li>
           </ul>
         </div>

         </div>
        )
      }else{
        if(type=="textarea"){
         return <pre onClick={this.changeEdit.bind(this)}>{(val&&val.length>0)?val: placeholder}</pre>
        }else{
         return <span onClick={this.changeEdit.bind(this)}>{(val&&val.length>0)?val: placeholder}</span>
        }
      }
    }
}

class Subnav extends React.Component {
  render(){
    const {addQuestion, changePaperType, paperType} = this.props

    return <div className="col-md-2">
           <div className="panel panel-default">
           <p>
            Choose Type:
           </p>
           <p>
            <button className="btn btn-default" onClick={()=>{addQuestion("RADIO")}}>Single Choice</button>
           </p>
           <p>
             <button className="btn btn-default" onClick={()=>{addQuestion("CHECKBOX")}}>Multiple Choice</button>
           </p>

          {paperType == "PAPER"?
            <p>Please choose the default right answer</p>:null
          }
          </div>

      </div>
  }
}


class SurveyQuestion extends React.Component {
  constructor(props){
    super(props)
    const {item} = this.props
    this.state = {
      title: item.title?item.title:"title",
      type: item.type,
      description:item.description?item.description:"",
      choices: item.choices?item.choices:['choice 1', 'choice 2' ],
      checked: item.checked?item.checked:item.type=="RADIO"?0:[],
    }

    this.update = this.update.bind(this)
    this.deleteChoice = this.deleteChoice.bind(this)
    this.moveChoiveUp = this.moveChoiveUp.bind(this)
    this.moveChoiveDown = this.moveChoiveDown.bind(this)
  }

  componentWillReceiveProps(newProps){
    this.setState(newProps.item)
  }

  update(){
    const {updateQuestion, index} = this.props
    let item = this.state 
    item.id = index
    updateQuestion(item)
  }

  updateTitle(val){
    const {updateQuestion, index} = this.props
    let item = JSON.parse( JSON.stringify(this.state) )
    item.index = index
    item.title = val
    updateQuestion(item)
  }

  updateChoice(idx, val){
    const {updateQuestion, index} = this.props
    let item = JSON.parse( JSON.stringify(this.state) )
    item.index = index
    item.choices[idx] = val
    updateQuestion(item)
  }

  updateDefaultCheckedRadio(idx){
    const {updateQuestion, index} = this.props
    let item = JSON.parse( JSON.stringify(this.state) )
    item.index = index
    item.checked = idx
    updateQuestion(item)
  }

  updateDefaultCheckedCheckbox(idx, checked){
    const {updateQuestion, index} = this.props
    let item = JSON.parse( JSON.stringify(this.state) )
    item.index = index

    if (checked){
      item.checked.push(idx)
      item.checked = Array.from(new Set(item.checked))
    }else{
      item.checked.splice(item.checked.indexOf(idx), 1)
    }
    updateQuestion(item)
  }


  //updateCheckedItem(idx)

  addChoice(){
    const {updateQuestion, index} = this.props
    //let item = this.state 
    let item = JSON.parse( JSON.stringify(this.state) )
    item.index = index
    item.choices.push('choice new')
    updateQuestion(item)
  }

  deleteChoice(idx){
    const {updateQuestion, index} = this.props
    //let item = this.state 
    let item = JSON.parse( JSON.stringify(this.state) )
    item.index = index
    item.choices.splice(idx, 1)
    updateQuestion(item)
  }

  moveChoiveUp(idx){
    const {updateQuestion, index} = this.props
    if(idx ==0){
      return 
    }
    let item = JSON.parse( JSON.stringify(this.state) )
    item.index = index
    item.choices[idx-1] = item.choices.splice(idx, 1, item.choices[idx-1])[0]
    updateQuestion(item)
  }

  moveChoiveDown(idx){

    const {updateQuestion, index} = this.props
    let item = JSON.parse( JSON.stringify(this.state) )

    if(idx==item.choices.length-1){
      return 
    }else{

    item.index = index
    item.choices[idx+1] = item.choices.splice(idx, 1, item.choices[idx+1])[0]
    updateQuestion(item)
    }

  }

  render(){
    const {item, deleteQuestion, index, paperType} = this.props

    return <div className="panel panel-default survey-question">
      <div className="panel-heading">
        Q{index+1}. {` `}
        <FormEdit 
          onFinish={(val)=>{this.updateTitle(val)}}
        val={this.state.title}/>
      </div>
      <div className="panel-body">
        {this.state.choices.map((i, index)=>{
          return <div className="survey-question__choice" key={index}>
          {
            this.state.type=="RADIO"? <input 
                type="radio"
                className="radio"
                disabled={paperType=="SURVEY"}
                onChange={()=>{this.updateDefaultCheckedRadio(index)}}
                checked={index == this.state.checked} aria-label="..."/>:
              <input 
                type="checkbox"
                className="radio"
                disabled={paperType=="SURVEY"}
                onChange={(evt)=>{
                  this.updateDefaultCheckedCheckbox(index, evt.target.checked)
                }}
                checked={this.state.checked.indexOf(index)>=0} aria-label="..."/>
          }
            <ChoiceEdit 
              key={index}
              onFinish={(val)=>{this.updateChoice(index, val)}}
              onMoveDown={this.moveChoiveDown.bind(this, index)}
              onMoveUp={this.moveChoiveUp.bind(this, index)}
              onDelete={this.deleteChoice.bind(this, index)}
            val={i}/>
          </div>
        })}
        
      </div>
      <div className="panel-footer">
        <button className="btn btn-default" onClick={this.addChoice.bind(this, index)} >
          <span className="glyphicon glyphicon-plus"></span>
        </button>
        <button className="delete-btn btn btn-default" onClick={deleteQuestion.bind(this, index)} >
          <span className="glyphicon glyphicon-trash"></span>
        </button>
      </div>
    </div>
  }
}

class Survey extends React.Component {
  constructor(props){
    super(props)
    this.state = {
      paperType: window.location.href.match(/questionnaire\?type=(\w+)/)[1].indexOf('surve')>=0?"SURVEY":"PAPER",
      list: [],
      title: "Please Enter Title",
      description:"Please Enter Subtitle"
    }
    this.changePaperType = this.changePaperType.bind(this)
    this.addQuestion = this.addQuestion.bind(this)
    this.deleteQuestion = this.deleteQuestion.bind(this)
    this.updateQuestion = this.updateQuestion.bind(this)
  }

  changePaperType(){
    this.setState({paperType: this.state.paperType=="SURVEY"?"PAPER":"SURVEY"})
  }

  addQuestion(type){
    this.setState({list: [...this.state.list, {type: type}]})
  }


  deleteQuestion(index){
    //let newList = Object.assgin({}, this.state.list)
    let newList = JSON.parse( JSON.stringify(this.state.list) )
    newList.splice(index, 1)
    this.setState({list: newList})
  }

  updateQuestion(item){
    let newList = JSON.parse( JSON.stringify(this.state.list) )
    newList.splice(item.index, 1, item)
    this.setState({list: newList})
  }

  updateTitle(val){
    this.setState({title: val})
  }

  updateDescription(val){
    this.setState({description: val})
  }

  submit(){
    let postData
    if(this.state.paperType=="SURVEY"){
      postData = this.state.list.map(i=>{
        return {
          name: i.title,
          choices: i.choices,
          multichoice: i.type=="RADIO"?"no":"yes",
        }
      })
    }else{
      postData = this.state.list.map(i=>{
        let choices = i.choices
        if (i.type == "RADIO"){
          choices = choices.map((j, index)=>{
            return {name:j, value: index==i.checked?1:0}
          })
        }else{
          choices = choices.map((j, index)=>{
            return {name: j, value: index in i.checked?1:0}
          })
        }

        return {
          name: i.title,
          choices: choices,
          multichoice: i.type=="RADIO"?"no":"yes",
        }
      })
    
    }

    let gid = window.location.href.match(/group\/show\/(\d+)/)[1];
    let fullPostData = {
      //user: "test", //mock
      gid: gid,
      type: this.state.paperType == "SURVEY"?'survey':'paper',
      name: this.state.title,
      desc: this.state.description,
      data: postData,
      questionAmount: postData.length,
    }

    axios.post('/group/'+ gid +'/questionnaire', qs.stringify(fullPostData))
    .then(result=>{
      alert('submit success')
    })
    .catch(res=>{
      alert('submit failed', res)
    })
  }

  render(){
    return <div className="panel panel-default">


        <Subnav 
          addQuestion={this.addQuestion}
          paperType={this.state.paperType}
          changePaperType={this.changePaperType}

          />
        <div className="col-md-10">

          <div className="survey__title">
            <FormEdit
              onFinish={(val)=>{this.updateTitle(val)}}
              val={this.state.title}/>
          </div>
          <div className="survey__subtitle">
            <FormEdit
              onFinish={(val)=>{this.updateDescription(val)}}
              val = {this.state.description}/>
          </div>


          {this.state.list.map((i, index)=>{
            return <SurveyQuestion 
              key={index} 
              index={index}
              paperType={this.state.paperType}
              item={i} 
              deleteQuestion={this.deleteQuestion}
              updateQuestion={this.updateQuestion}
              />
          })}
        <button  className="btn btn-default" onClick={this.submit.bind(this)}> submit </button>
        </div>
        <div style={{clear: 'both'}}> </div>

      </div>
  }
}

render(<Survey />, document.getElementById('test-survey'));

