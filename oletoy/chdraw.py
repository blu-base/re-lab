# Copyright (C) 2007-2013	Valek Filippov (frob@df.ru)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of version 3 or later of the GNU General Public
# License as published by the Free Software Foundation.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301
# USA
#

import sys,struct
from utils import *

ids = {
	0x0001:'CreationUserName',
	0x0002:'CreationDate',
	0x0003:'CreationProgram',
	0x0004:'ModificationUserName',
	0x0005:'ModificationDate',
	0x0006:'ModificationProgram',
	0x0007:'Unused1',
	0x0008:'Name',
	0x0009:'Comment',
	0x000A:'ZOrder',
	0x000B:'RegistryNumber',
	0x000C:'RegistryAuthority',
	0x000D:'Unused2',
	0x000E:'RepresentsProperty',
	0x000F:'IgnoreWarnings',
	0x0010:'ChemicalWarning',
	0x0011:'Visible',
	0x0100:'FontTable',
	0x0200:'2DPosition',
	0x0201:'3DPosition',
	0x0202:'2DExtent',
	0x0203:'3DExtent',
	0x0204:'BoundingBox',
	0x0205:'RotationAngle',
	0x0206:'BoundsInParent',
	0x0207:'3DHead',
	0x0208:'3DTail',
	0x0209:'TopLeft',
	0x020A:'TopRight',
	0x020B:'BottomRight',
	0x020C:'BottomLeft',
	0x0300:'ColorTable',
	0x0301:'ForegroundColor',
	0x0302:'BackgroundColor',
	0x0400:'Node_Type',
	0x0401:'Node_LabelDisplay',
	0x0402:'Node_Element',
	0x0403:'Atom_ElementList',
	0x0404:'Atom_Formula',
	0x0420:'Atom_Isotope',
	0x0421:'Atom_Charge',
	0x0422:'Atom_Radical',
	0x0423:'Atom_RestrictFreeSites',
	0x0424:'Atom_RestrictImplicitHydrogens',
	0x0425:'Atom_RestrictRingBondCount',
	0x0426:'Atom_RestrictUnsaturatedBonds',
	0x0427:'Atom_RestrictRxnChange',
	0x0428:'Atom_RestrictRxnStereo',
	0x0429:'Atom_AbnormalValence',
	0x042A:'Unused3',
	0x042B:'Atom_NumHydrogens',
	0x042C:'Unused4',
	0x042D:'Unused5',
	0x042E:'Atom_HDot',
	0x042F:'Atom_HDash',
	0x0430:'Atom_Geometry',
	0x0431:'Atom_BondOrdering',
	0x0432:'Node_Attachments',
	0x0433:'Atom_GenericNickname',
	0x0434:'Atom_AltGroupID',
	0x0435:'Atom_RestrictSubstituentsUpTo',
	0x0436:'Atom_RestrictSubstituentsExactly',
	0x0437:'Atom_CIPStereochemistry',
	0x0438:'Atom_Translation',
	0x0439:'Atom_AtomNumber',
	0x043A:'Atom_ShowQuery',
	0x043B:'Atom_ShowStereo',
	0x043C:'Atom_ShowAtomNumber',
	0x043D:'Atom_LinkCountLow',
	0x043E:'Atom_LinkCountHigh',
	0x043F:'Atom_IsotopicAbundance',
	0x0440:'Atom_ExternalConnectionType',
	0x0500:'Mole_Racemic',
	0x0501:'Mole_Absolute',
	0x0502:'Mole_Relative',
	0x0503:'Mole_Formula',
	0x0504:'Mole_Weight',
	0x0505:'Frag_ConnectionOrder',
	0x0600:'Bond_Order',
	0x0601:'Bond_Display',
	0x0602:'Bond_Display2',
	0x0603:'Bond_DoublePosition',
	0x0604:'Bond_Begin',
	0x0605:'Bond_End',
	0x0606:'Bond_RestrictTopology',
	0x0607:'Bond_RestrictRxnParticipation',
	0x0608:'Bond_BeginAttach',
	0x0609:'Bond_EndAttach',
	0x060A:'Bond_CIPStereochemistry',
	0x060B:'Bond_BondOrdering',
	0x060C:'Bond_ShowQuery',
	0x060D:'Bond_ShowStereo',
	0x060E:'Bond_CrossingBonds',
	0x060F:'Bond_ShowRxn',
	0x0700:'Text',
	0x0701:'Justification',
	0x0702:'LineHeight',
	0x0703:'WordWrapWidth',
	0x0704:'LineStarts',
	0x0705:'LabelAlignment',
	0x0706:'LabelLineHeight',
	0x0707:'CaptionLineHeight',
	0x0708:'InterpretChemically',
	0x0800:'MacPrintInfo',
	0x0801:'WinPrintInfo',
	0x0802:'PrintMargins',
	0x0803:'ChainAngle',
	0x0804:'BondSpacing',
	0x0805:'BondLength',
	0x0806:'BoldWidth',
	0x0807:'LineWidth',
	0x0808:'MarginWidth',
	0x0809:'HashSpacing',
	0x080A:'LabelStyle',
	0x080B:'CaptionStyle',
	0x080C:'CaptionJustification',
	0x080D:'FractionalWidths',
	0x080E:'Magnification',
	0x080F:'WidthPages',
	0x0810:'HeightPages',
	0x0811:'DrawingSpaceType',
	0x0812:'Width',
	0x0813:'Height',
	0x0814:'PageOverlap',
	0x0815:'Header',
	0x0816:'HeaderPosition',
	0x0817:'Footer',
	0x0818:'FooterPosition',
	0x0819:'PrintTrimMarks',
	0x081A:'LabelStyleFont',
	0x081B:'CaptionStyleFont',
	0x081C:'LabelStyleSize',
	0x081D:'CaptionStyleSize',
	0x081E:'LabelStyleFace',
	0x081F:'CaptionStyleFace',
	0x0820:'LabelStyleColor',
	0x0821:'CaptionStyleColor',
	0x0822:'BondSpacingAbs',
	0x0823:'LabelJustification',
	0x0824:'FixInplaceExtent',
	0x0825:'Side',
	0x0826:'FixInplaceGap',
	0x0900:'Window_IsZoomed',
	0x0901:'Window_Position',
	0x0902:'Window_Size',
	0x0A00:'Graphic_Type',
	0x0A01:'Line_Type',
	0x0A02:'Arrow_Type',
	0x0A03:'Rectangle_Type',
	0x0A04:'Oval_Type',
	0x0A05:'Orbital_Type',
	0x0A06:'Bracket_Type',
	0x0A07:'Symbol_Type',
	0x0A08:'Curve_Type',
	0x0A20:'Arrow_HeadSize',
	0x0A21:'Arc_AngularSize',
	0x0A22:'Bracket_LipSize',
	0x0A23:'Curve_Points',
	0x0A24:'Bracket_Usage',
	0x0A25:'Polymer_RepeatPattern',
	0x0A26:'Polymer_FlipType',
	0x0A27:'BracketedObjects',
	0x0A28:'Bracket_RepeatCount',
	0x0A29:'Bracket_ComponentOrder',
	0x0A2A:'Bracket_SRULabel',
	0x0A2B:'Bracket_GraphicID',
	0x0A2C:'Bracket_BondID',
	0x0A2D:'Bracket_InnerAtomID',
	0x0A2E:'Curve_Points3D',
	0x0A60:'Picture_Edition',
	0x0A61:'Picture_EditionAlias',
	0x0A62:'MacPICT',
	0x0A63:'WindowsMetafile',
	0x0A64:'OLEObject',
	0x0A65:'EnhancedMetafile',
	0x0A80:'Spectrum_XSpacing',
	0x0A81:'Spectrum_XLow',
	0x0A82:'Spectrum_XType',
	0x0A83:'Spectrum_YType',
	0x0A84:'Spectrum_XAxisLabel',
	0x0A85:'Spectrum_YAxisLabel',
	0x0A86:'Spectrum_DataPoint',
	0x0A87:'Spectrum_Class',
	0x0A88:'Spectrum_YLow',
	0x0A89:'Spectrum_YScale',
	0x0AA0:'TLC_OriginFraction',
	0x0AA1:'TLC_SolventFrontFraction',
	0x0AA2:'TLC_ShowOrigin',
	0x0AA3:'TLC_ShowSolventFront',
	0x0AA4:'TLC_ShowBorders',
	0x0AA5:'TLC_ShowSideTicks',
	0x0AB0:'TLC_Rf',
	0x0AB1:'TLC_Tail',
	0x0AB2:'TLC_ShowRf',
	0x0B00:'NamedAlternativeGroup_TextFrame',
	0x0B01:'NamedAlternativeGroup_GroupFrame',
	0x0B02:'NamedAlternativeGroup_Valence',
	0x0B80:'GeometricFeature',
	0x0B81:'RelationValue',
	0x0B82:'BasisObjects',
	0x0B83:'ConstraintType',
	0x0B84:'ConstraintMin',
	0x0B85:'ConstraintMax',
	0x0B86:'IgnoreUnconnectedAtoms',
	0x0B87:'DihedralIsChiral',
	0x0B88:'PointIsDirected',
	0x0C00:'ReactionStep_Atom_Map',
	0x0C01:'ReactionStep_Reactants',
	0x0C02:'ReactionStep_Products',
	0x0C03:'ReactionStep_Plusses',
	0x0C04:'ReactionStep_Arrows',
	0x0C05:'ReactionStep_ObjectsAboveArrow',
	0x0C06:'ReactionStep_ObjectsBelowArrow',
	0x0C07:'ReactionStep_Atom_Map_Manual',
	0x0C08:'ReactionStep_Atom_Map_Auto',
	0x0D00:'ObjectTag_Type',
	0x0D01:'Unused6',
	0x0D02:'Unused7',
	0x0D03:'ObjectTag_Tracking',
	0x0D04:'ObjectTag_Persistent',
	0x0D05:'ObjectTag_Value',
	0x0D06:'Positioning',
	0x0D07:'PositioningAngle',
	0x0D08:'PositioningOffset',
	0x0E00:'Sequence_Identifier',
	0x0F00:'CrossReference_Container',
	0x0F01:'CrossReference_Document',
	0x0F02:'CrossReference_Identifier',
	0x0F03:'CrossReference_Sequence',
	0x1000:'Template_PaneHeight',
	0x1001:'Template_NumRows',
	0x1002:'Template_NumColumns',
	0x1100:'Group_Integral',
	0x1FF0:'SplitterPositions',
	0x1FF1:'PageDefinition',
	0x8000:'Document',
	0x8001:'Page',
	0x8002:'Group',
	0x8003:'Fragment',
	0x8004:'Node',
	0x8005:'Bond',
	0x8006:'Text',
	0x8007:'Graphic',
	0x8008:'Curve',
	0x8009:'EmbeddedObject',
	0x800a:'NamedAlternativeGroup',
	0x800b:'TemplateGrid',
	0x800c:'RegistryNumber',
	0x800d:'ReactionScheme',
	0x800e:'ReactionStep',
	0x800f:'ObjectDefinition',
	0x8010:'Spectrum',
	0x8011:'ObjectTag',
	0x8012:'OleClientItem',
	0x8013:'Sequence',
	0x8014:'CrossReference',
	0x8015:'Splitter',
	0x8016:'Table',
	0x8017:'BracketedGroup',
	0x8018:'BracketAttachment',
	0x8019:'CrossingBond',
	0x8020:'Border',
	0x8021:'Geometry',
	0x8022:'Constraint',
	0x8023:'TLCPlate',
	0x8024:'TLCLane',
	0x8025:'TLCSpot',
	0x8FFF:'UnknownObject'
}

def open (page,buf,parent):
	piter = []
	if parent == None:
		parent = add_pgiter(page,"File","chdraw","file",buf,parent)
	off = 0x1c
	add_pgiter(page,"Signature","chdraw","sig",buf[:0x1c],parent)
	while off < len(buf):
		tag = struct.unpack('<H', buf[off:off+2])[0]
		off += 2
		if tag in ids:
			tname = ids[tag]
		else:
			tname = "Type: %04x"%tag
		if tag&0x8000:
			rid = struct.unpack('<I', buf[off:off+4])[0]
			parent = add_pgiter(page,"%s ID: %04x"%(tname,rid),"chdraw",rid,"",parent)
			off += 4
		elif tag == 0:
			try:
				parent = page.model.iter_parent(parent)
			except:
				pass
		else:
			rlen = struct.unpack('<H', buf[off:off+2])[0]
			off += 2
			data = buf[off:off+rlen]
			add_pgiter(page,tname,"chdraw",tag,data,parent)
			off += rlen
