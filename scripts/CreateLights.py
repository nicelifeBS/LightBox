#python

import modo
import lx

scene = modo.scene.current()

def create_light(name=None, type='areaLight'):

    if not name:
        # Create temp user value and ask user
        # for light name        
        lx.eval('user.defNew LightCreate.name type:string life:momentary')
        lx.eval('user.value LightCreate.name value:AreaLight')
        lx.eval('user.def LightCreate.name dialogname "Light Name"')
        lx.eval('user.value LightCreate.name')
        name = lx.eval('user.value LightCreate.name ?')

    s = []
    lx.eval('item.create locator name:%s_LOC' % name)
    s += scene.selectedByType(modo.constants.LOCATOR_TYPE)
    lx.eval('item.create areaLight name:%s_AL' % name)
    s += scene.selectedByType(modo.constants.AREALIGHT_TYPE)

    if len(s) == 2:
        lx.eval('item.parent %s %s 0 inPlace:1' % (s[1].id, s[0].id))

        # create direction constrain
        scene.select(s[1])
        scene.select(s[0], add=True)		
        lx.eval('constraintDirection')


args = lx.args()[0]
if args == 'areaLight':
    create_light(type='areaLight')