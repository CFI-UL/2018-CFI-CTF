import React, { Component } from 'react'
import { FlatList, StyleSheet, View, Text } from 'react-native'
import PropTypes from 'prop-types'

export default class FlagList extends Component {
  renderItem = ({ item }) => {
    return (
      <View style={styles.text}>
        <Text style={styles.flag}>{item}</Text>
      </View>  
    )
  }
  
  ListEmptyComponent = () => {
    return (
      <Text style={styles.emptyListText}>
        You have no flag in your collection yet.
      </Text>
    )
  }
  
  render () {
    const { flags } = this.props
    return (
      <View style={styles.container}>
        <FlatList 
          data={flags}
          keyExtractor={item => item}
          renderItem={this.renderItem}
          ListEmptyComponent={this.ListEmptyComponent}/>
      </View>    
    )
  }
}

FlagList.propTypes = {
  flags: PropTypes.array.isRequired
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    flexDirection: 'row',
    backgroundColor: '#4e4e4e',
    margin: 16,
    padding: 8
  },
  emptyListText: {
    textAlign: 'center',
    color: '#fff',
    fontSize: 16,
    marginBottom: 5,
  },
  flag: {
    textAlign: 'center',
    color: '#fff',
    marginBottom: 5,
    fontSize: 16,
    fontFamily: 'monospace'
  },
})