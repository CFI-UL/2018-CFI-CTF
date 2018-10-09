import React, { Component } from 'react';
import { Image, StyleSheet, Text, View } from 'react-native';
import FlagList from './FlagList'
import SubmitFlagButton from './SubmitFlagButton'

const logoPath = '../assets/images/logo.png'

export default class App extends Component<Props> {
  constructor (props) {
    super(props)
    
    this.state = { 
      flags: [] 
    }
  }
  
  onSubmitSuccess = (flag) => {
      this.setState({
        flags: this.state.flags.concat([ flag ])
      })
  }
  
  render() {
    const { flags } = this.state
    return (
      <View style={styles.container}>
        <Image style={styles.logo} source={require(logoPath)}/>
        <View style={styles.section}>
          <FlagList flags={flags}/>
          <SubmitFlagButton onSubmitSuccess={this.onSubmitSuccess}/>
        </View>
      </View>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'space-between',
    alignItems: 'center',
    backgroundColor: '#0e0e0e',
    paddingTop: 16,
    paddingBottom: 16
  },
  section: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 8
  },
  text: {
    textAlign: 'center',
    color: '#fff',
    marginBottom: 5,
  },
  logo: {
    width: 222,
    height: 288
  }
})
