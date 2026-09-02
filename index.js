// ponytail: minimal entry so the native build resolves an entry file. The JS app is not under test.
import { registerRootComponent } from 'expo';
import { Text } from 'react-native';
registerRootComponent(() => <Text>AGP 9 new DSL compatibility runner</Text>);
