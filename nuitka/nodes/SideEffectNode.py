#     Copyright 2012, Kay Hayen, mailto:kay.hayen@gmail.com
#
#     Part of "Nuitka", an optimizing Python compiler that is compatible and
#     integrates with CPython, but also works on its own.
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.
#
""" Node that models side effects.

Sometimes, the effect of an expression needs to be had, but the value itself does
not matter at all.
"""

from .NodeBases import CPythonExpressionChildrenHavingBase


class CPythonExpressionSideEffects( CPythonExpressionChildrenHavingBase ):
    kind = "EXPRESSION_SIDE_EFFECTS"

    named_children = ( "side_effects", "expression" )

    def __init__( self, side_effects, expression, source_ref ):
        CPythonExpressionChildrenHavingBase.__init__(
            self,
            values = {
                "side_effects" : tuple( side_effects ),
                "expression"   : expression
            },
            source_ref = source_ref
        )

    getSideEffects  = CPythonExpressionChildrenHavingBase.childGetter( "side_effects" )
    getExpression = CPythonExpressionChildrenHavingBase.childGetter( "expression" )

    setSideEffects  = CPythonExpressionChildrenHavingBase.childSetter( "side_effects" )

    def setChild( self, name, value ):
        if name == "side_effects":
            real_value = []

            for child in value:
                if child.isExpressionSideEffects():
                    real_value.extend( child.getSideEffects() )
                    real_value.append( child.getExpression() )
                else:
                    assert child.isExpression()

                    real_value.append( child )

            value = real_value

        return CPythonExpressionChildrenHavingBase.setChild( self, name, value )

    def computeNode( self, constraint_collection ):
        side_effects = self.getSideEffects()
        new_side_effects = []

        for side_effect in side_effects:
            if side_effect.mayHaveSideEffects( constraint_collection ):
                new_side_effects.append( side_effect )

        if new_side_effects != side_effects:
            self.setSideEffects( new_side_effects )

        if not new_side_effects:
            return self.getExpression(), "new_expression", "Removed empty side effects."

        return self, None, None
