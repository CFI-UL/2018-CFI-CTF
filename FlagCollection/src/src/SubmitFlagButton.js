import React, { Component,Fragment } from 'react'
import { 
  Modal, 
  View, 
  Text, 
  TextInput, 
  Button, 
  StyleSheet,
  ToastAndroid
} from 'react-native'
import { validateFlag } from './FlagValidator'
import PropTypes from 'prop-types'

export default class SubmitFlagButton extends Component {
  constructor (props) {
    super(props)
    
    this.state = { flag: '', displayModal: false }
  }
  
  hideModal = () => {
    this.setState({ displayModal: false })
  }
  
  showModal = () => {
    this.setState({ displayModal: true })
  }
    
  submitFlag = () => {
    const { flag } = this.state
    validateFlag(flag).then((valid) => {
      if (valid) {
        ToastAndroid.show(
          'Good job!', 
          ToastAndroid.SHORT
        )
        this.props.onSubmitSuccess(flag)
        this.hideModal()
      } else {
        ToastAndroid.show(
          'Invalid flag! Try harder!', 
          ToastAndroid.SHORT
        )
      }
      this.setState({ flag: '' })
    })
  }
  
  render () {
    const { flag, displayModal } = this.state
    return (
      <Fragment>
        <Button 
          title="Submit flag"
          color="red"
          onPress={this.showModal}/>
          <Modal
            animationType="fade"
            transparent={true}
            visible={displayModal}
            onRequestClose={this.hideModal}>
            <View style={styles.modal}>
              <View>
                <Text style={styles.title}>SUBMIT FLAG</Text>
                <TextInput
                  style={styles.input}
                  placeholder="Flag"
                  onChangeText={(flag) => this.setState({flag})}
                  value={flag}
                  />
                <Button 
                  title="Submit"
                  color="red"
                  onPress={this.submitFlag}/>
              </View>
            </View>
          </Modal>
        </Fragment>  
    )
  }
}

SubmitFlagButton.propTypes = {
  onSubmitSuccess: PropTypes.func.isRequired
}

const styles = StyleSheet.create({
  modal: {
    flex: 1,
    backgroundColor: '#0e0e0e',
    padding: 16
  },
  title: {
    textAlign: 'center',
    color: '#fff',
    fontSize: 16,
    marginBottom: 16,
    fontWeight: 'bold'
  },
  input: {
    height: 40, 
    borderColor: '#4e4e4e', 
    backgroundColor: '#fff',
    borderWidth: 1,
    marginBottom: 16
  }
})